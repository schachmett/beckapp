 
# Beckapp

"Simple" backup script that utilizes the great [Borg Backup](https://borgbackup.readthedocs.io) and [rsync](https://linux.die.net/man/1/rsync) to put files away safely. Key points:

* Configurable with a [yaml](https://yaml.org/)-file
* Runs every 30 min or so to check if a backup is due
* Mounts backup locations or sources automatically:
	- network shares can be defined in the [fstab](https://wiki.archlinux.de/title/Fstab)
	- LUKS encrypted partitions are mounted automatically
	- ssh access is tested for rsync, might not work for borg (yet, but should be easy to implement)
* Runs as a specified user

## Installation

Copy the files as follows:

```sh
$ sudo cp beckapp /usr/local/bin/
$ sudo mkdir /usr/local/etc/backup
$ sudo cp backup.yaml /usr/local/etc/backup/
```

I suggest to place config files like encryption keys for borg repositories or LUKS partitions also into `/usr/local/etc/backup` and make them owned by root with permissions `400`

Then, activate the systemd timer:

```sh
$ sudo cp beckapp.service beckapp.timer /etc/systemd/system
$ systemctl enable --now beckapp.timer
```

## Usage

```sh
usage: beckapp [-h] [-j JOB [JOB ...]] [-w] [-v] [-l LOG_NUMBER] [-y] [-f]
               [--ignore-pre] [--log-path LOG_PATH]
               {backup,schedule,showlog,mount,status,debug}

Do borg and rsync backups

positional arguments:
  {backup,schedule,showlog,mount,status,debug}

optional arguments:
  -h, --help            show this help message and exit
  -j JOB [JOB ...], --job JOB [JOB ...]
  -w, --watch-log
  -v, --verbose
  -l LOG_NUMBER, --log-number LOG_NUMBER
  -y, --confirm-yes
  -f, --force-backup
  --ignore-pre
  --log-path LOG_PATH
```

If `-j` is not given, all jobs defined in the `backup.yaml` file are assumed.

For an example configuration, see `example_backup.yaml`