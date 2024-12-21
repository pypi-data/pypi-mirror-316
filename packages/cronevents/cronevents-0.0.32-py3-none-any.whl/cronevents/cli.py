import argparse
import os
import sys

import cronevents.event_manager
import cronevents.register


service_name = 'cronevents-manager.service'
suggested_service_path = f'/etc/systemd/system/{service_name}'
system_service_config = '''
[Unit]
Description=Handler to manaage Cron Events using the cronevents package
After=network.target

[Service]
WorkingDirectory={{path}}
ExecStart=/bin/bash -c 'source venv/bin/activate && cronevents manager'
Type=simple
RemainAfterExit=no
Restart=always
RestartSec=5s

[Install]
WantedBy=multi-user.target
'''
service_commands = f'''
First , create a service file at {suggested_service_path} with the following content:
run: `cronevents service-file --path {"{{path}}"} > {suggested_service_path}`

Then make changes as needed:
run: `sudo nano {suggested_service_path}`

Then reload the systemd daemon:
run: `sudo systemctl daemon-reload`

Then start the service:
run: `sudo systemctl start {service_name}`

To check the status of the service:
run: `sudo systemctl status {service_name}`

To enable the service on boot:
run: `sudo systemctl enable {service_name}`
'''


def cli():
    parser = argparse.ArgumentParser(description='Buelon command-line interface')
    parser.add_argument('-v', '--version', action='version', version='Cron Events 0.0.32')

    subparsers = parser.add_subparsers(title='Commands', dest='command', required=False)

    # Hub command
    hub_parser = subparsers.add_parser('manager', help='Run the hub')
    hub_parser.add_argument('-p', '--postgres', required=False, help='Postgres connection (host:port:user:password:database)')

    # Register command
    register_parser = subparsers.add_parser('register', help='Register a new event')
    register_parser.add_argument('-p', '--postgres', required=False, help='Postgres connection (host:port:user:password:database)')
    register_parser.add_argument('-f', '--file', required=True, help='Python file path with event decorators')

    #  Service command
    service_parser = subparsers.add_parser('service-file', help='Prints service file')
    service_parser.add_argument('-p', '--path', help='Path to project')

    #  Service command
    service_parser = subparsers.add_parser('service', help='Prints service commands')
    service_parser.add_argument('-p', '--path', help='Path to project')

    # Parse arguments
    args, remaining_args = parser.parse_known_args()
    # Handle the commands
    if args.command == 'manager':
        if args.postgres:
            os.environ['CRON_EVENTS_USING_POSTGRES'] = 'true'
            (os.environ['POSTGRES_HOST'], os.environ['POSTGRES_PORT'], os.environ['POSTGRES_USER'],
             os.environ['POSTGRES_PASSWORD'], os.environ['POSTGRES_DATABASE']) = args.postgres.split(':')
        cronevents.event_manager.main()
    if args.command == 'register':
        if args.postgres:
            os.environ['CRON_EVENTS_USING_POSTGRES'] = 'true'
            (os.environ['POSTGRES_HOST'], os.environ['POSTGRES_PORT'], os.environ['POSTGRES_USER'],
             os.environ['POSTGRES_PASSWORD'], os.environ['POSTGRES_DATABASE']) = args.postgres.split(':')

        cronevents.register.register_events(args.file, args.postgres)
    if args.command == 'service-file':
        print(system_service_config.replace('{{path}}', args.path or os.getcwd()))
    if args.command == 'service':
        print(service_commands.replace('{{path}}', args.path or os.getcwd()))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    cli()
