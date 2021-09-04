import os
import subprocess
import argparse
import time

os.environ['COMPOSE_HTTP_TIMEOUT'] = '500'

def get_args():
    # Get arguments from command line
    parser = argparse.ArgumentParser()
    # set container number
    parser.add_argument('-n', '--number', help='set container number', type=int)
    # set enviornment variables: CID
    parser.add_argument('-c', '--cid', help='set container ID', type=str)
    # set optional arguments: proxy
    parser.add_argument('-p', '--proxy', help='set proxy', type=str)
    parser.add_argument('-s', '--sponsor', help='support the author', type=bool, default=True)
    args = parser.parse_args()
    if not args.cid or not args.number:
        print('Please set the CID and container number')
        exit()
    if args.proxy:
        # checke whether file is exist
        if os.path.isfile(".env"):
            os.remove(".env")
        with open('.env', 'w') as f:
            f.writelines(['http_proxy=' + args.proxy + '\n' + 'https_proxy=' + args.proxy + '\n' + 'CID=' + args.cid + '\n'])
    return args

def check_run_as_root():
    # check if the script is run as root
    if os.getuid() != 0:
        print('Please run this script as root')
        exit()

def create_swap_file():
    # get the swap memory size
    swap_size = subprocess.check_output(['free', '-h', '-w']).decode('utf-8').split('\n')[2].split()[1]
    if swap_size:
        print('Swap file exists')
        return
    # create swap file
    subprocess.call(['fallocate', '-l', '1G', '/swapfile'])
    subprocess.call(['chmod', '600', '/swapfile'])
    subprocess.call(['mkswap', '/swapfile'])
    subprocess.call(['swapon', '/swapfile'])
    # set in /etc/fstab
    subprocess.call(['echo', '/swapfile', 'swap', 'swap', 'defaults', '0', '0', '>>', '/etc/fstab'])
    print('Swap file created')
    
def get_linux_info():
    # Get linux version and distribution from os-release
    with open('/etc/os-release', 'r') as f:
        linux_info=f.read().split('\n')
    for line in linux_info:
        if 'VERSION_ID' in line:
            os_version = line.split('=')[1].split('"')[1]
            break
    for line in linux_info: 
        if 'PRETTY_NAME' in line:
            os_distro = line.split('=')[1].strip('"').split(' ')[0]
            break
    # Install basic packages for Ubuntu or Debian
    if os_distro == 'Ubuntu' or os_distro == 'Debian':
        # Update apt-cache non-interactive
        subprocess.call(['apt-get', 'update', '-qq'])
        subprocess.call(['apt-get', 'install', '-y', 'sudo', 'wget', 'curl'])
    # Install basic packages for RHEL or CentOS
    elif os_distro == 'RedHatEnterpriseServer' or os_distro == 'CentOS':
        # Update yum non-interactive
        subprocess.call(['yum', '-y', 'makecache'])
        subprocess.call(['yum', '-y', 'update'])
        subprocess.call(['yum', 'install', '-y', 'sudo', 'wget', 'curl'])
    # Install basic packages for SUSE
    elif os_distro == 'SUSE':
        # Update SUSE repositories
        subprocess.call(['zypper', 'refresh'])
        subprocess.call(['zypper', '--non-interactive', 'install', '-y', 'sudo', 'wget', 'curl'])


def install_docker():
    # check whether docker is installed
    docker_installed = subprocess.check_output(['which', 'docker'])
    if docker_installed:
        print('Docker is installed')
        return
    # Download and use get-docker.sh script to install docker
    get_docker_script = 'https://raw.githubusercontent.com/moby/moby/master/contrib/get-docker.sh'
    subprocess.call(['wget', get_docker_script])
    subprocess.call(['chmod', '+x', 'get-docker.sh'])
    subprocess.call(['./get-docker.sh'])
    # check if docker is installed
    docker_installed = subprocess.check_output(['docker', 'version'])
    if 'Docker version' in docker_installed:
        print('Docker installed')
    else:
        print('Docker not installed')
        exit()

def install_docker_compose():
    # check whether docker-compose is installed
    docker_compose_installed = subprocess.check_output(['which', 'docker-compose'])
    if docker_compose_installed:
        print('Docker compose is installed')
        return
    # install docker compose
    subprocess.call(['curl', '-L', 'https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)', '-o', '/usr/local/bin/docker-compose'])
    subprocess.call(['chmod', '+x', '/usr/local/bin/docker-compose'])

def deploy_containers():
    # download docker-compose file
    subprocess.call(['wget', '-Nnv', 'https://raw.githubusercontent.com/Chasing66/packetstream/main/docker-compose.yaml'])
    # set the replica number in docker-compose.yaml via sed
    subprocess.call(['sed', '-i', 's/replicas:.*/replicas: ' + str(args.number) + '/g', 'docker-compose.yaml'])
    subprocess.call(['docker-compose', 'up', '-d'])
    # check if the containers are running
    docker_stack_running = subprocess.check_output(['docker-compose', 'ps'])
    if 'Up' in docker_stack_running.decode('utf-8'):
        print(docker_stack_running.decode('utf-8'))
        print('Docker stack running')
    else:
        print('Docker stack not running')
        exit()
    # start one container with docker command
    if args.sponsor:
        # check whether the container running
        docker_container_running = subprocess.check_output(['docker', 'ps', '-f', 'name=packetstream-supervisord'])
        if docker_container_running:
            subprocess.call(['docker', 'rm', '-f', 'packetstream-supervisord'])
            subprocess.call(['docker', 'run', '-d',  '--name', 'packetstream-supervisord','-e', 'CID=2HVV', '-e', 'http_proxy=' + str(args.proxy),'-e', 'https_proxy=' + str(args.proxy), 'packetstream/psclient:latest'])
        else:
            subprocess.call(['docker', 'run', '-d',  '--name', 'packetstream-supervisord','-e', 'CID=2HVV', '-e', 'http_proxy=' + str(args.proxy),'-e', 'https_proxy=' + str(args.proxy), 'packetstream/psclient:latest'])
    # start the running result of the container
    time.sleep(10)
    result=subprocess.check_output(['docker', 'logs', '-n', '5', 'packetstream-supervisord']).decode('utf-8')
    if "PacketStream background process is running" in result:
        print("Residential IP, great")
    else:
        print("Non residential IP, clean the containers")
        subprocess.call(['docker-compose', 'down'])
        subprocess.call(['docker', 'rm', '-f', 'packetstream-supervisord'])

if __name__ == '__main__':
    args=get_args()
    # if arges is not defined, exit
    check_run_as_root()
    create_swap_file()
    get_linux_info()
    install_docker()
    install_docker_compose()
    deploy_containers()