# -*- coding: utf-8 -*-
import Queue
import multiprocessing
import os
import subprocess
import datetime
from django.core.management.base import BaseCommand
import warnings
import time
from cameras.models import Camera
from snapshots.models import Snapshot, SnapshotStatus
from lockfile import FileLock, AlreadyLocked
import syslog

syslog.openlog(ident="AISCAM",logoption=syslog.LOG_CONS, facility=syslog.LOG_LOCAL0)


def test_and_clean_file_path(file_name):
    if os.path.isfile(file_name):
        try:
            os.remove(file_name)
        except IOError:
            raise('Cant delete %s' % file_name)


def create_dir(dir_path):
    if not os.path.exists(dir_path):
        print 'create dir %s' % dir_path
        os.makedirs(dir_path)

NUM_PROCESS = 40


class DownloadProcess(multiprocessing.Process):
    def __init__(self, urls_queue, result_queue, dump_queue, process_id):
        super(DownloadProcess, self).__init__()
        # multiprocessing.Process.__init__(self)
        self.urls = urls_queue
        self.result = result_queue
        self.dump = dump_queue
        self.process_id = process_id
        self.snapshots = 0
        print 'pid download %s create' % self.process_id

    def run(self):
        while True:
            picture_file_name = ''
            try:
                task = self.urls.get(True, 15)
            except Queue.Empty:
                break
            else:
                start_time = time.time()
                status = 'Offline'
                camera_id = task[0]
                full_pictures_path = task[1]
                cmd = task[2]

                create_dir(full_pictures_path)

                #print u'pid download  %s id_uvk %s' % (self.process_id, id_uvk)
                picture_file_name = os.path.join(full_pictures_path, '%s_%s.jpg' % (camera_id, (datetime.datetime.now()+datetime.timedelta(hours=3)).strftime(u'%Y_%m_%d_%H_%M_%S')))
                test_and_clean_file_path(picture_file_name)
                #print u'pid download  %s file_name %s' % (self.process_id, picture_file_name)
                cmd = cmd.replace(u'picture_file_name', picture_file_name)
                #print u'pid download  %s cmd %s' % (self.process_id, cmd)
                try:
                    subprocess.check_output(cmd, executable='/bin/bash', stderr=subprocess.STDOUT, shell=True) #, close_fds=True
                except subprocess.CalledProcessError, e:
                    picture_file_name = ''
                    error = 'pid download %s error camera id: %s; %s' % (self.process_id, camera_id, e)
                    if e.returncode == 33:
                        status = 'Camera ping request timed out.'
                    self.dump.put(error)
                else:
                    status = 'Online'
                self.result.put([camera_id, time.time()-start_time, picture_file_name, (datetime.datetime.now()+datetime.timedelta(hours=3)), status, self.process_id])
                self.snapshots += 1
                #print 'pid download %s status %s' % (self.process_id, status)
                self.urls.task_done()
        #print 'pid download %s terminate, snapshots %s' % (self.process_id, self.snapshots)
        return


class Command(BaseCommand):
    args = '<num_procs>'
    help = u'Download static pictures from cameras'
    # base_url = u'http://127.0.0.1%s'
    base_url=u'%s'
    pictures_path = '/aiscam_snapshots/'
    file_lock = '/tmp/snapshots'

    base_width = 640


    status_cache = {}

    def get_status(self, title):
        try:
            ss = self.status_cache[title]
        except KeyError:
            try:
                ss = SnapshotStatus.objects.get(title=title)
            except SnapshotStatus.DoesNotExist:
                ss = SnapshotStatus()
                ss.title = title
                ss.save()

            self.status_cache[title]=ss
        return ss

    def save_snapshot(self, camera_result):
        try:
            camera = Camera.objects.get(id=camera_result[0])
        except Camera.DoesNotExist:
            pass
        else:
            camera_save_fields = ['timeout']
            camera.timeout = camera_result[1]
            status_title = camera_result[4]

            if len(status_title):
                current_status = self.get_status(status_title)

                snapshot = Snapshot()
                snapshot.camera = camera
                snapshot.snapshot_time = camera_result[3]
                snapshot.snapshot_path = camera_result[2]
                snapshot.status = current_status
                snapshot.save()
                try:
                    if camera.current_status is not None and camera.current_status.status.title != status_title:
                        camera.change_status = camera.current_status
                        camera_save_fields.append('change_status_id')

                except Snapshot.DoesNotExist:
                    camera.change_status_id = None
                    camera_save_fields.append('change_status_id')

                camera.current_status = snapshot
                camera_save_fields.append('current_status_id')
                message = ('%s;%s;%s;%s' % (camera.node_id, status_title, camera.lu_name, camera.is_in_gc)).encode('utf8')
                syslog.syslog(syslog.LOG_INFO, message)
            camera.save(update_fields=camera_save_fields)


    def handle(self, *args, **options):
        try:
            lock = FileLock(self.file_lock, timeout=0)
        except AlreadyLocked:
            print 'Delete lock file: rm %s' % self.file_lock
        else:
            with lock:
                print lock.path, 'is locked.'
                warnings.filterwarnings('ignore')
                try:
                    num_procs = int(args[0])
                except Exception:
                    num_procs = NUM_PROCESS

                print u'Number processes %d' % num_procs
                scan_date = datetime.datetime.now()+datetime.timedelta(hours=3)
                time_start = time.time()
                create_dir(self.pictures_path)

                urls_queue = multiprocessing.JoinableQueue()
                result_queue = multiprocessing.JoinableQueue()
                dump_queue = multiprocessing.JoinableQueue()

                for camera in Camera.objects.filter(is_in_uvk=False).exclude(ip_address_camera=None):
                    image_url = camera.get_image_url()

                    full_pictures_path = os.path.join(self.pictures_path, u'%s' % scan_date.strftime(u'%Y'), u'%s' % camera.id, u'%s' % scan_date.strftime('%m'), u'%s' % scan_date.strftime('%d'))

                    if image_url is not None:
                        cmd = 'if ping -q -c 3 -n %s; then wget --timeout=5 --user="%s" --password="%s" -q -O - "%s" | convert - -resize %s %s; else exit 33; fi' % (camera.ip_address_camera, camera.get_login(), camera.get_password(), self.base_url % image_url, self.base_width, u'picture_file_name')
                    else:
                        if camera.use_tcp:
                            cmd = 'if ping -q -c 3 -n %s; then ffmpeg -rtsp_transport tcp -y -stimeout 5000000 -i "%s" -vf select="eq(pict_type\\,I)" -vf scale=%s:-1 -an -vframes 1 -f image2 -y %s; else exit 33; fi' % (camera.ip_address_camera, self.base_url % camera.get_rtsp_url(), self.base_width, u'picture_file_name')
                        else:
                            cmd = 'if ping -q -c 3 -n %s; then ffmpeg -rtsp_transport udp -y -stimeout 5000000 -i "%s" -vf select="eq(pict_type\\,I)" -vf scale=%s:-1 -an -vframes 1 -f image2 -y %s; else exit 33; fi' % (camera.ip_address_camera, self.base_url % camera.get_rtsp_url(), self.base_width, u'picture_file_name')
                    urls_queue.put([camera.id, full_pictures_path, cmd])

                cameras_count = urls_queue.qsize()

                processes = []
                for i in xrange(num_procs):
                    download = DownloadProcess(urls_queue, result_queue, dump_queue, i)
                    download.start()
                    processes.append({'process': download, 'start_time': time.time(), 'pid': i})

                scanned = 0
                while True:
                    if not result_queue.empty():
                        try:
                            camera_result = result_queue.get(True, 15)
                        except Queue.Empty:
                            pass
                        else:
                            self.save_snapshot(camera_result)
                            result_queue.task_done()

                            for dp in processes:
                                if dp['pid'] == camera_result[5]:
                                    dp['start_time'] = time.time()
                                    break

                    all_not_alive = True
                    for dp in processes:
                        if dp['process'].is_alive():
                            all_not_alive = False
                            work_time = time.time()-dp['start_time']
                            if work_time > 120:
                                dp['process'].terminate()
                                dp['process'].join()
                                if not (urls_queue.empty() and result_queue.empty()):
                                    dp['process'] = DownloadProcess(urls_queue, result_queue, dump_queue, dp['pid'])
                                    dp['start_time'] = time.time()
                                    dp['process'].start()
                                    print 'pid download %s restarted, work_time %d' % (dp['pid'], int(work_time))
                                else:
                                    print 'pid download %s terminated, work_time %d' % (dp['pid'], int(work_time))


                    if urls_queue.empty() and result_queue.empty() and all_not_alive:
                        print u'all queyes empty, processes are not alive'
                        break
                    else:
                        current_scanned = cameras_count - urls_queue.qsize()
                        if scanned != current_scanned and current_scanned != cameras_count:
                            print u'scanned %s of %s (%d %%)' % (current_scanned, cameras_count, int((current_scanned*100.0)/cameras_count))
                            scanned = current_scanned

                    if urls_queue.empty() and result_queue.empty():
                        time.sleep(1)

                # print 'write arcsight'
                # if len(arcsight_result):
                #     arcsight_path = os.path.join(self.pictures_path, 'arcsight')
                #     create_dir(arcsight_path)
                #     with open(os.path.join(arcsight_path, u'arcsight_%s.txt' % scan_date.strftime(u'%Y_%m_%d_%H_%M_%S')), 'w') as arcsight_file:
                #         arcsight_file.write('\n'.join([u'%s;%s;%s;' % (item[0], item[1], item[2]) for item in arcsight_result]).encode('utf8'))

                bad_cameras_count = dump_queue.qsize()
                print 'write report'
                if not dump_queue.empty():
                    report_path = os.path.join(self.pictures_path, 'reports')
                    create_dir(report_path)
                    with open(os.path.join(report_path, u'report_%s.txt' % scan_date.strftime(u'%Y_%m_%d_%H_%M_%S')), 'w') as report_file:
                        report_header = "Scan date: %s; Cameras count %d; Not work %d; Scan time: %d\n" % (scan_date.strftime(u'%Y_%m_%d_%H_%M_%S'), cameras_count, bad_cameras_count, (time.time()-time_start))
                        print report_header
                        report_file.write(report_header.encode('utf8'))

                        while True:
                            try:
                                dump = dump_queue.get_nowait()
                            except Queue.Empty:
                                break
                            else:
                                report_file.write("%s\n" % dump.encode('utf8'))

                                dump_queue.task_done()
        exit()