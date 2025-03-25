import logging
import random
from datetime import datetime, timedelta
from typing import Any, Dict

from faker import Faker

from data_generator import DataGenerator

fake = Faker()
logger = logging.getLogger(__name__)


def generate_random_process_execution(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random security.process_executions record.

    Args:
        id_fields: Dictionary containing predetermined ID fields
                  (security_process_execution_id, security_host_id)
        dg: DataGenerator instance

    Returns:
        Dict containing a random process execution record
        (without ID fields)
    """
    # Host ID must be provided
    security_host_id = id_fields.get('security_host_id')
    if not security_host_id:
        raise ValueError("security_host_id is required")

    # Get host information - this is deterministic since we have the PK
    host_info = get_host_info(security_host_id, dg)

    # Determine if Windows or Linux based on host info
    is_windows = False
    if host_info and 'os' in host_info:
        is_windows = 'windows' in host_info['os'].lower()

    # Get users associated with this host - deterministic through FK relationships
    host_users = get_host_users(security_host_id, dg)

    # Define process selection logic
    if is_windows:
        process_options = get_windows_processes()
    else:
        process_options = get_linux_processes()

    # Select a process based on host characteristics
    process_info = select_process_for_host(process_options, host_info, dg)

    # Determine the user for this process
    if process_info["user"]:
        # Use the fixed system user if defined for this process
        user_name = process_info["user"]
    elif host_users:
        # Use a user from the ones linked to this host through security.accounts
        user_name = select_user_for_process(host_users, process_info, is_windows, security_host_id, dg)
    else:
        # If no linked users found (shouldn't happen with proper FK relationships)
        user_name = get_default_user(is_windows)

    # Process information
    process_name = process_info["name"]
    command_line = process_info["cmd"]

    # Process ID generation - use a deterministic approach based on host
    process_id = generate_process_id(security_host_id, process_name)

    # Parent process ID - deterministic based on process type
    parent_process_id = determine_parent_process_id(process_name, is_windows, security_host_id)

    # Generate timestamps
    now = datetime.now()

    # Start time based on host uptime if available
    if 'last_seen' in host_info:
        try:
            host_last_seen = datetime.fromisoformat(host_info['last_seen'].replace('Z', '+00:00'))
            max_age = (now - host_last_seen).total_seconds()
            start_time = now - timedelta(seconds=random.randint(0, int(max_age)))
        except (ValueError, TypeError):
            # Fallback if last_seen is invalid
            start_time = now - timedelta(hours=random.randint(1, 168))
    else:
        # Fallback: Start time between 1 hour and 7 days ago
        start_time = now - timedelta(hours=random.randint(1, 168))

    # End time based on process type
    is_running = False

    # System processes and services typically run until system restart
    long_running_processes = [
        "svchost.exe", "systemd", "lsass.exe", "services.exe", "csrss.exe",
        "apache2", "nginx", "mysqld", "postgres", "dockerd", "containerd",
        "cron", "rsyslogd", "explorer.exe"
    ]

    if process_name in long_running_processes:
        # 90% chance still running
        is_running = random.random() < 0.9

    # Interactive applications
    interactive_processes = [
        "chrome.exe", "firefox.exe", "msedge.exe", "powershell.exe", "cmd.exe",
        "bash", "python3", "java", "node"
    ]

    if process_name in interactive_processes:
        # 30% chance still running
        is_running = random.random() < 0.3

    # Other processes (5% chance still running)
    if process_name not in long_running_processes and process_name not in interactive_processes:
        is_running = random.random() < 0.05

    # Set end time based on running status
    if is_running:
        end_time = None
    else:
        # Determine appropriate duration based on process type
        if process_name in long_running_processes:
            max_duration = int((now - start_time).total_seconds() * 0.9)
            duration = random.randint(max_duration // 2, max_duration) if max_duration > 0 else 1
        elif process_name in interactive_processes:
            max_duration = min(int((now - start_time).total_seconds()), 8 * 60 * 60)
            duration = random.randint(60, max_duration) if max_duration > 60 else 60
        else:
            max_duration = min(int((now - start_time).total_seconds()), 30 * 60)
            duration = random.randint(1, max_duration) if max_duration > 1 else 1

        # Calculate end time as a datetime
        end_time = start_time + timedelta(seconds=duration)

    # Construct the process execution record (without ID fields)
    process_execution = {
        "process_name": process_name,
        "process_id": process_id,
        "parent_process_id": parent_process_id,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat() if end_time is not None else None,
        "command_line": command_line,
        "user_name": user_name
    }

    return process_execution


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

    except Exception as e:
        # Handle database errors gracefully
        logger.error(e)

    # If no result or error, return bare minimum
    return {'os': 'linux', 'hostname': f'unknown-{host_id}'}


def get_host_users(host_id: Any, dg: DataGenerator) -> list:
    """
    Get users deterministically associated with a host through FK relationships,
    with a fallback to random enterprise associates
    """
    users = []

    try:
        # Try to get users that have accessed this host through file access events
        query = """
        SELECT DISTINCT i.name, i.service_account 
        FROM security.file_accesses fa
        JOIN security.process_executions pe ON fa.security_process_execution_id = pe.security_process_execution_id
        JOIN security.accounts a ON pe.user_name = a.name
        JOIN security.identities i ON a.security_identity_id = i.security_identity_id
        WHERE fa.security_system_id = %s
        """

        with dg.conn.cursor() as cursor:
            cursor.execute(query, (host_id,))
            for row in cursor.fetchall():
                if row.get('name'):  # Ensure name is not None
                    users.append(row)

        # If no users found, try through network connections
        if not users:
            query = """
            SELECT DISTINCT i.name, i.service_account 
            FROM security.network_connections nc
            JOIN security.process_executions pe ON nc.security_process_execution_id = pe.security_process_execution_id
            JOIN security.accounts a ON pe.user_name = a.name
            JOIN security.identities i ON a.security_identity_id = i.security_identity_id
            WHERE nc.security_host_id = %s
            """

            with dg.conn.cursor() as cursor:
                cursor.execute(query, (host_id,))
                for row in cursor.fetchall():
                    if row.get('name'):  # Ensure name is not None
                        users.append(row)

        # If still no users found, get users from process executions directly
        if not users:
            query = """
            SELECT DISTINCT user_name
            FROM security.process_executions
            WHERE security_host_id = %s AND user_name IS NOT NULL
            """

            with dg.conn.cursor() as cursor:
                cursor.execute(query, (host_id,))
                for row in cursor.fetchall():
                    if row.get('name'):  # Ensure name is not None
                        users.append({'name': row['name'], 'is_service': False})

        # If still no users found, get some random enterprise associates
        if not users:
            # Get 2-3 random associates as potential users
            num_associates = random.randint(2, 3)
            query = """
            SELECT first_name, last_name
            FROM enterprise.associates
            ORDER BY RANDOM()
            LIMIT %s
            """

            with dg.conn.cursor() as cursor:
                cursor.execute(query, (num_associates,))
                for row in cursor.fetchall():
                    if row[0] and row[1]:  # Ensure names are not None
                        # Create a username from first name and first letter of last name
                        username = f"{row[0].lower()}{row[1][0].lower()}"
                        users.append({'name': username, 'is_service': False})

    except Exception as e:
        # Handle database errors gracefully
        logger.error(e)

    # Add some system users appropriate for the OS type (as fallbacks)
    os_info = get_host_info(host_id, dg).get('os', '').lower()
    if 'windows' in os_info:
        for sys_user in ["SYSTEM", "Administrator", "LocalService", "NetworkService"]:
            if not any(u['name'] == sys_user for u in users):
                users.append({'name': sys_user, 'is_service': True})
    else:
        for sys_user in ["root", "nobody", "www-data", "systemd-network"]:
            if not any(u['name'] == sys_user for u in users):
                users.append({'name': sys_user, 'is_service': True})

    return users


def get_windows_processes():
    """Return standard Windows process definitions"""
    return [
        {"name": "svchost.exe", "cmd": "svchost.exe -k LocalServiceNetworkRestricted -p", "user": "SYSTEM"},
        {"name": "explorer.exe", "cmd": "C:\\Windows\\explorer.exe", "user": None},
        {"name": "chrome.exe", "cmd": "\"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\" --type=renderer",
         "user": None},
        {"name": "firefox.exe", "cmd": "\"C:\\Program Files\\Mozilla Firefox\\firefox.exe\"", "user": None},
        {"name": "msedge.exe",
         "cmd": "\"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe\" --type=renderer", "user": None},
        {"name": "wmiprvse.exe", "cmd": "C:\\Windows\\System32\\wbem\\wmiprvse.exe", "user": "SYSTEM"},
        {"name": "csrss.exe", "cmd": "%SystemRoot%\\System32\\csrss.exe ObjectDirectory=\\Windows", "user": "SYSTEM"},
        {"name": "lsass.exe", "cmd": "C:\\Windows\\System32\\lsass.exe", "user": "SYSTEM"},
        {"name": "services.exe", "cmd": "C:\\Windows\\System32\\services.exe", "user": "SYSTEM"},
        {"name": "powershell.exe", "cmd": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -NoProfile",
         "user": None},
        {"name": "cmd.exe", "cmd": "C:\\Windows\\System32\\cmd.exe", "user": None},
        {"name": "RuntimeBroker.exe", "cmd": "C:\\Windows\\System32\\RuntimeBroker.exe -Embedding", "user": None},
        {"name": "dllhost.exe",
         "cmd": "C:\\Windows\\System32\\dllhost.exe /Processid:{97deaadf-e03e-4e2e-b2d5-039a7e64c3fa}", "user": None},
        {"name": "taskhostw.exe", "cmd": "taskhostw.exe {222A245B-E637-4AE9-A93F-A59CA119A75E}", "user": None},
        {"name": "SearchIndexer.exe", "cmd": "C:\\Windows\\System32\\SearchIndexer.exe /Embedding", "user": "SYSTEM"}
    ]


def get_linux_processes():
    """Return standard Linux process definitions"""
    return [
        {"name": "systemd", "cmd": "/usr/lib/systemd/systemd --system --deserialize 17", "user": "root"},
        {"name": "sshd", "cmd": "/usr/sbin/sshd -D", "user": "root"},
        {"name": "apache2", "cmd": "/usr/sbin/apache2 -k start", "user": "www-data"},
        {"name": "nginx", "cmd": "nginx: master process /usr/sbin/nginx -g daemon on; master_process on;",
         "user": "www-data"},
        {"name": "mysqld", "cmd": "/usr/sbin/mysqld", "user": "mysql"},
        {"name": "postgres", "cmd": "/usr/lib/postgresql/12/bin/postgres -D /var/lib/postgresql/12/main",
         "user": "postgres"},
        {"name": "bash", "cmd": "-bash", "user": None},
        {"name": "python3", "cmd": "python3 /usr/local/bin/gunicorn app:app", "user": None},
        {"name": "java", "cmd": "java -Xmx2048m -jar /opt/application/app.jar", "user": None},
        {"name": "dockerd", "cmd": "/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock",
         "user": "root"},
        {"name": "containerd", "cmd": "/usr/bin/containerd", "user": "root"},
        {"name": "cron", "cmd": "/usr/sbin/cron -f", "user": "root"},
        {"name": "rsyslogd", "cmd": "/usr/sbin/rsyslogd -n", "user": "root"},
        {"name": "docker-proxy",
         "cmd": "/usr/bin/docker-proxy -proto tcp -host-ip 0.0.0.0 -host-port 80 -container-ip 172.17.0.2 -container-port 80",
         "user": "root"},
        {"name": "node", "cmd": "node /var/www/app/server.js", "user": "nodejs"}
    ]


def select_process_for_host(process_options, host_info, _dg: DataGenerator):
    """
    Deterministically select a process for a host based on host characteristics
    """
    # Use a seed from the host_id to make the selection deterministic
    host_id_str = str(host_info.get('hostname', ''))
    seed = sum(ord(c) for c in host_id_str) % len(process_options)
    random.seed(seed)

    # Certain processes should only appear on servers
    server_processes = ["sshd", "apache2", "nginx", "mysqld", "postgres", "dockerd"]
    workstation_processes = ["chrome.exe", "firefox.exe", "msedge.exe", "explorer.exe"]

    is_server = host_info.get('system_type', '').lower() == 'server'

    # Filter process list based on host type
    if is_server:
        # Remove workstation-specific processes for servers
        filtered_processes = [p for p in process_options if p["name"] not in workstation_processes]
    else:
        # Remove server-specific processes for workstations
        filtered_processes = [p for p in process_options if p["name"] not in server_processes]

    # If filtering removed all options, revert to original list
    if not filtered_processes:
        filtered_processes = process_options

    # Select a process using our seed
    return random.choice(filtered_processes)


def select_user_for_process(host_users, process_info, is_windows, host_id, dg):
    """
    Select a user for a process with weighting toward host owner and some randomness
    """
    process_name = process_info["name"]

    # System processes need system users
    if process_name in ["svchost.exe", "csrss.exe", "lsass.exe", "services.exe", "systemd", "sshd"]:
        return "SYSTEM" if is_windows else "root"

    # Service processes need service users
    if process_name in ["apache2", "nginx", "mysqld", "postgres"]:
        service_map = {
            "apache2": "www-data",
            "nginx": "www-data",
            "mysqld": "mysql",
            "postgres": "postgres"
        }
        return service_map.get(process_name, "www-data")

    # Get host owner if available
    host_owner = get_host_owner(host_id, dg)

    # Check for interactive processes that would likely be run by regular users
    is_interactive_process = process_name in [
        "chrome.exe", "firefox.exe", "msedge.exe", "powershell.exe", "cmd.exe",
        "bash", "python3", "vim", "nano", "sh", "node"
    ]

    if is_interactive_process:
        # 70% chance to use host owner if available
        if host_owner and random.random() < 0.7:
            return host_owner

        # 20% chance to use a linked user account
        elif host_users and random.random() < 0.2:
            # Prefer non-service accounts for interactive processes
            user_accounts = [u for u in host_users if not u.get('is_service', False)]
            user_list = user_accounts if user_accounts else host_users
            return random.choice(user_list)['name']

        # 10% chance to use a random associate from enterprise
        else:
            random_associate = get_random_associate(dg)
            if random_associate:
                return random_associate
            # Fallback if no random associate found
            elif host_users:
                return random.choice(host_users)['name']
            else:
                return get_default_user(is_windows)
    else:
        # For non-interactive processes, follow previous logic
        user_accounts = [u for u in host_users if not u.get('is_service', False)]

        if user_accounts:
            # Deterministically pick a user based on process name
            seed = sum(ord(c) for c in process_name) % len(user_accounts)
            return user_accounts[seed]['name']
        elif host_users:
            # Fall back to any available user
            seed = sum(ord(c) for c in process_name) % len(host_users)
            return host_users[seed]['name']
        else:
            # No users available, use system default
            return get_default_user(is_windows)


def get_host_owner(host_id, dg):
    """
    Get the username of the host owner
    """
    if not host_id:
        return None

    try:
        # Query for asset owner information directly from hosts table
        query = """
        SELECT asset_owner_name
        FROM security.hosts
        WHERE security_host_id = %s AND asset_owner_name IS NOT NULL
        """

        with dg.conn.cursor() as cursor:
            cursor.execute(query, (host_id,))
            result = cursor.fetchone()

        if result and result.get('asset_owner_name'):
            return result.get('asset_owner_name')

        # If no asset owner, try to find owner through process executions on this host
        query = """
        SELECT DISTINCT user_name
        FROM security.process_executions
        WHERE security_host_id = %s AND user_name IS NOT NULL
        AND user_name NOT IN ('SYSTEM', 'root', 'www-data', 'nobody', 'mysql', 'postgres')
        LIMIT 1
        """

        with dg.conn.cursor() as cursor:
            cursor.execute(query, (host_id,))
            result = cursor.fetchone()

        if result and result.get('user_name'):
            return result.get('user_name')

        # Last resort - try to find a relevant associate
        query = """
        SELECT first_name || last_name AS fullname
        FROM enterprise.associates
        ORDER BY RANDOM()
        LIMIT 1
        """

        with dg.conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()

        if result and result.get('fullname'):
            return result.get('fullname').lower()

    except Exception as e:
        # Handle database errors gracefully
        logger.error(e)

    return None


def get_random_associate(dg):
    """
    Get a random username from enterprise.associates
    """
    try:
        # Query for a random associate
        query = """
        SELECT first_name, last_name
        FROM enterprise.associates
        ORDER BY RANDOM()
        LIMIT 1
        """

        with dg.conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()

        if result:
            # Create username from first name and first character of last name
            username = f"{result.get('first_name', '').lower()}{result.get('last_name', 'X')[0].lower()}"
            return username

    except Exception as e:
        logger.error(e)

    return None


def get_default_user(is_windows):
    """Return default system user based on OS"""
    return "SYSTEM" if is_windows else "root"


def generate_process_id(host_id, process_name):
    """
    Generate a deterministic process ID based on host ID and process name
    """
    # Use the host ID and process name to create a deterministic seed
    seed = str(host_id) + process_name
    seed_value = sum(ord(c) for c in seed)

    # Generate PID in a common range (avoiding system PIDs)
    return (seed_value % 60000) + 1000


def determine_parent_process_id(process_name, is_windows, host_id):
    """
    Determine a parent process ID based on process type
    """
    # Common parent processes by OS
    if is_windows:
        system_parents = {
            "svchost.exe": 4,
            "csrss.exe": 4,
            "lsass.exe": 4,
            "services.exe": 4,
            "explorer.exe": 4,
            "dllhost.exe": 4
        }
        user_parents = {
            "chrome.exe": "explorer.exe",
            "firefox.exe": "explorer.exe",
            "msedge.exe": "explorer.exe",
            "powershell.exe": "explorer.exe",
            "cmd.exe": "explorer.exe"
        }
    else:
        system_parents = {
            "systemd": 1,
            "sshd": 1,
            "apache2": 1,
            "nginx": 1,
            "mysqld": 1,
            "postgres": 1,
            "dockerd": 1,
            "containerd": 1,
            "cron": 1,
            "rsyslogd": 1
        }
        user_parents = {
            "bash": "sshd",
            "python3": "bash",
            "java": "bash",
            "node": "bash"
        }

    # Determine parent based on process type
    if process_name in system_parents:
        return system_parents[process_name]
    elif process_name in user_parents:
        parent_name = user_parents[process_name]
        # Calculate parent PID using the same deterministic function
        return generate_process_id(host_id, parent_name)
    else:
        # Default parent
        return 1 if not is_windows else 4


def calculate_end_time(process_name, start_time, now):
    """
    Calculate an end time for a process based on its type
    """
    # System processes and services typically run until system restart
    long_running_processes = [
        "svchost.exe", "systemd", "lsass.exe", "services.exe", "csrss.exe",
        "apache2", "nginx", "mysqld", "postgres", "dockerd", "containerd",
        "cron", "rsyslogd", "explorer.exe"
    ]

    if process_name in long_running_processes:
        # 90% chance still running, 10% chance terminated
        if random.random() < 0.9:
            return None
        else:
            max_duration = int((now - start_time).total_seconds() * 0.9)
            duration = random.randint(max_duration // 2, max_duration) if max_duration > 0 else 1
            return start_time + timedelta(seconds=duration)

    # Interactive applications
    interactive_processes = [
        "chrome.exe", "firefox.exe", "msedge.exe", "powershell.exe", "cmd.exe",
        "bash", "python3", "java", "node"
    ]

    if process_name in interactive_processes:
        # 30% chance still running, 70% chance terminated
        if random.random() < 0.3:
            return None
        else:
            # Typically run for minutes to hours
            max_duration = min(int((now - start_time).total_seconds()), 8 * 60 * 60)
            duration = random.randint(60, max_duration) if max_duration > 60 else 60
            return start_time + timedelta(seconds=duration)

    # Other processes (short-lived)
    # 5% chance still running, 95% chance terminated
    if random.random() < 0.05:
        return None
    else:
        # Typically run for seconds to minutes
        max_duration = min(int((now - start_time).total_seconds()), 30 * 60)
        duration = random.randint(1, max_duration) if max_duration > 1 else 1
        return start_time + timedelta(seconds=duration)
