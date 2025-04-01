from data_generator import DataGenerator, SkipRowGenerationError
from datetime import datetime, timedelta
from faker import Faker
from fsi_data_generator.fsi_generators.intelligent_generators.security.agent_status import \
    AgentStatus
from fsi_data_generator.fsi_generators.intelligent_generators.security.service_status import \
    ServiceStatus
from fsi_data_generator.fsi_generators.intelligent_generators.security.system_status import \
    SystemType
from typing import Any, Dict

import logging
import psycopg2
import random
import sys

fake = Faker()
logger = logging.getLogger(__name__)
prev_services = set()


def generate_random_running_service(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random security.running_services record.

    Args:
        id_fields: Dictionary containing predetermined ID fields
                  (security_host_id)
        dg: DataGenerator instance

    Returns:
        Dict containing a random running service record
        (without ID fields)
    """
    # We need security_host_id to generate a service
    security_host_id = id_fields.get('security_host_id')
    if not security_host_id:
        raise ValueError("security_host_id is required")

    # Get host information to determine OS-appropriate services
    host_info = get_host_info(security_host_id, dg)

    # Determine if Windows or Linux based on host info
    is_windows = False
    if host_info and 'os' in host_info:
        is_windows = 'windows' in host_info['os'].lower()

    # Get system type from host info
    if host_info and 'system_type' in host_info:
        try:
            system_type = SystemType(host_info['system_type'])
        except (ValueError, TypeError):
            # If system_type isn't valid or is None
            system_type = SystemType.SERVER
    else:
        system_type = SystemType.SERVER

    # Define common services based on OS
    if is_windows:
        service_options = get_windows_services(system_type)
    else:
        service_options = get_linux_services(system_type)

    # Select a service name appropriate for this host
    running_service_name = select_service_for_host(service_options, host_info)

    # Generate start time
    now = datetime.now()

    # Services typically start at boot time or when the system has been running for a while
    # Get last_seen from host_info if available to estimate system uptime
    if host_info and 'last_seen' in host_info:
        try:
            last_seen = datetime.fromisoformat(host_info['last_seen'].replace('Z', '+00:00'))
            # Assume system uptime is between 1 day and last_seen
            max_uptime = (now - last_seen).total_seconds() + (86400 * 30)  # Add 30 days max
            start_time = now - timedelta(seconds=random.randint(86400, int(max_uptime)))
        except (ValueError, TypeError):
            # Fallback if last_seen is invalid
            start_time = now - timedelta(days=random.randint(1, 30))
    else:
        # Fallback: system uptime between 1 and 60 days
        start_time = now - timedelta(days=random.randint(1, 60))

    # Get agent status to determine typical service status
    if host_info and 'agent_status' in host_info:
        try:
            agent_status = AgentStatus(host_info['agent_status'])
        except (ValueError, TypeError):
            # Default to active if not found or not valid
            agent_status = AgentStatus.ACTIVE
    else:
        agent_status = AgentStatus.ACTIVE

    # Determine service status based on agent status
    status = ServiceStatus.get_random(agent_status)

    # Construct the running service record
    running_service = {
        "running_service_name": running_service_name,
        "start_time": start_time.isoformat(),
        "status": status.value  # Convert enum to string value
    }

    key = (security_host_id, running_service_name)
    global prev_services
    if key in prev_services:
        raise SkipRowGenerationError

    prev_services.add(key)

    return running_service


def get_host_info(host_id: Any, dg: DataGenerator) -> Dict[str, Any]:
    """
    Get host information using the PK
    """
    try:
        query = """
        SELECT hostname, os, os_version, system_type, last_seen, agent_status
        FROM security.hosts
        WHERE security_host_id = %s
        """

        with dg.conn.cursor() as cursor:
            cursor.execute(query, (host_id,))
            result = cursor.fetchone()

        return result

    except psycopg2.ProgrammingError as e:
        # Log the critical error
        logger.critical(f"Programming error detected in the SQL query: {e}")

        # Exit the program immediately with a non-zero status code
        sys.exit(1)


def get_windows_services(system_type: SystemType) -> list:
    """
    Get Windows services appropriate for the system type
    """
    # Common Windows services across all system types
    common_services = [
        "wuauserv",  # Windows Update
        "Dnscache",  # DNS Client
        "Dhcp",  # DHCP Client
        "LanmanWorkstation",  # Workstation
        "LanmanServer",  # Server
        "EventLog",  # Windows Event Log
        "MpsSvc",  # Windows Firewall
        "WinDefend",  # Windows Defender
        "Schedule",  # Task Scheduler
        "BITS",  # Background Intelligent Transfer Service
        "Spooler",  # Print Spooler
        "wscsvc",  # Security Center
        "Power",  # Power service
        "W32Time",  # Windows Time
        "TrustedInstaller",  # Windows Modules Installer
        "CryptSvc",  # Cryptographic Services
    ]

    # Server-specific services
    server_services = [
        "MSSQLSERVER",  # SQL Server
        "SQLSERVERAGENT",  # SQL Server Agent
        "RpcSs",  # Remote Procedure Call
        "W3SVC",  # IIS Web Server
        "SMTP",  # SMTP Server
        "MSExchangeIS",  # Exchange Information Store
        "IISADMIN",  # IIS Admin
        "DFSR",  # DFS Replication
        "DNS",  # DNS Server
        "DHCPServer",  # DHCP Server
        "NtFrs",  # File Replication
        "Netlogon",  # Net Logon
        "RemoteAccess",  # Routing and Remote Access
        "RpcLocator",  # RPC Locator
        "MSMQ",  # Message Queuing
    ]

    # Workstation-specific services
    workstation_services = [
        "Audiosrv",  # Windows Audio
        "Themes",  # Themes
        "CDPUserSvc",  # Connected Devices Platform User Service
        "OneSyncSvc",  # Sync Host
        "WpnService",  # Windows Push Notifications
        "WpnUserService",  # Windows Push Notifications User Service
        "WlanSvc",  # WLAN AutoConfig
        "PcaSvc",  # Program Compatibility Assistant
        "BthAvctpSvc",  # Bluetooth Audio
        "BTAGService",  # Bluetooth Audio Gateway
        "TabletInputService",  # Touch Keyboard and Handwriting
        "PrintNotify",  # Printer Extensions and Notifications
    ]

    # Laptop-specific services
    laptop_services = workstation_services + [
        "SensrSvc",  # Sensor Service
        "SensorService",  # Sensor Monitoring Service
        "BatteryManager",  # Battery Management
        "BthHFSrv",  # Bluetooth Hands-Free
        "DisplayEnhancementService",  # Display Enhancement
        "WirelessDisplayService",  # Wireless Display
        "WifiCx",  # Wi-Fi Connectivity
        "NcdAutoSetup",  # Network Connected Devices Auto-Setup
    ]

    # Select appropriate services based on system type
    if system_type == SystemType.SERVER:
        return common_services + server_services
    elif system_type == SystemType.LAPTOP:
        return common_services + laptop_services
    elif system_type == SystemType.WORKSTATION:
        return common_services + workstation_services
    else:
        return common_services


def get_linux_services(system_type: SystemType) -> list:
    """
    Get Linux services appropriate for the system type
    """
    # Common Linux services across all system types
    common_services = [
        "systemd",  # System manager
        "systemd-journald",  # Journal service
        "systemd-logind",  # Login service
        "systemd-udevd",  # Device manager
        "dbus-daemon",  # D-Bus message bus
        "rsyslogd",  # System logging
        "chronyd",  # Time synchronization
        "sshd",  # SSH daemon
        "crond",  # Cron daemon
        "polkitd",  # Authorization manager
        "NetworkManager",  # Network manager
        "systemd-resolved",  # DNS resolver
        "tuned",  # System tuning
        "agetty",  # Terminal manager
        "auditd",  # Audit daemon
    ]

    # Server-specific services
    server_services = [
        "httpd",  # Apache web server
        "nginx",  # Nginx web server
        "mysqld",  # MySQL database
        "postgres",  # PostgreSQL database
        "mariadb",  # MariaDB database
        "named",  # BIND DNS server
        "smbd",  # Samba file sharing
        "nmbd",  # NetBIOS service
        "postfix",  # Mail transfer agent
        "dovecot",  # IMAP/POP3 server
        "nfs-server",  # NFS server
        "rpcbind",  # RPC port mapper
        "memcached",  # Memory caching
        "redis-server",  # Redis data store
        "mongod",  # MongoDB database
        "rabbitmq-server",  # RabbitMQ message broker
        "zookeeper",  # ZooKeeper service
        "tomcat",  # Tomcat application server
        "jenkins",  # Jenkins CI server
        "docker",  # Docker service
        "containerd",  # Container runtime
        "kubelet",  # Kubernetes node agent
    ]

    # Workstation-specific services
    workstation_services = [
        "gdm",  # GNOME Display Manager
        "lightdm",  # Light Display Manager
        "sddm",  # Simple Desktop Display Manager
        "xdm",  # X Display Manager
        "cups",  # Print service
        "avahi-daemon",  # mDNS/DNS-SD
        "bluetooth",  # Bluetooth service
        "pulseaudio",  # Audio service
        "snapd",  # Snap package manager
        "switcheroo-control",  # Graphics switching
        "wpa_supplicant",  # Wi-Fi authentication
        "ModemManager",  # Modem management
        "colord",  # Color management
    ]

    # Laptop-specific services
    laptop_services = workstation_services + [
        "thermald",  # Thermal management
        "power-profiles-daemon",  # Power profiles
        "tlp",  # TLP power management
        "bluetooth",  # Bluetooth service
        "iwd",  # Wireless daemon
    ]

    # Container/VM specific services
    container_services = [
        "docker",  # Docker daemon
        "containerd",  # Container runtime
        "dockerd",  # Docker daemon
        "kubelet",  # Kubernetes node agent
        "kube-proxy",  # Kubernetes network proxy
        "crio",  # Container Runtime Interface
        "envoy",  # Service proxy
        "istio",  # Service mesh
        "fluentd",  # Data collector
        "etcd",  # Key-value store
        "calico-node",  # Network policy engine
    ]

    # Select appropriate services based on system type
    if system_type == SystemType.SERVER:
        return common_services + server_services
    elif system_type == SystemType.LAPTOP:
        return common_services + laptop_services
    elif system_type == SystemType.WORKSTATION:
        return common_services + workstation_services
    elif system_type in [SystemType.VIRTUAL_MACHINE, SystemType.CONTAINER]:
        return common_services + container_services
    else:
        return common_services


def select_service_for_host(service_options: list, host_info: Dict[str, Any]) -> str:
    """
    Select a service that is appropriate for the host
    """
    # If no services to choose from, generate a generic one
    if not service_options:
        return f"service-{random.randint(1, 999)}"

    # Get host OS from host_info
    hostname = host_info.get('hostname', '') if host_info else ''

    # Special case: select services that match hostname patterns
    if 'db' in hostname and any(
            s in ['mysqld', 'postgres', 'mariadb', 'mongod', 'MSSQLSERVER'] for s in service_options):
        db_services = [s for s in service_options if s in ['mysqld', 'postgres', 'mariadb', 'mongod', 'MSSQLSERVER']]
        return random.choice(db_services)

    if 'web' in hostname and any(s in ['httpd', 'nginx', 'W3SVC', 'IISADMIN', 'tomcat'] for s in service_options):
        web_services = [s for s in service_options if s in ['httpd', 'nginx', 'W3SVC', 'IISADMIN', 'tomcat']]
        return random.choice(web_services)

    if 'mail' in hostname and any(s in ['postfix', 'dovecot', 'SMTP', 'MSExchangeIS'] for s in service_options):
        mail_services = [s for s in service_options if s in ['postfix', 'dovecot', 'SMTP', 'MSExchangeIS']]
        return random.choice(mail_services)

    # Otherwise, randomly select a service
    return random.choice(service_options)
