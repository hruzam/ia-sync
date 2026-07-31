# Service Management & Monitoring — @home Machine

**Location:** `~/.config/zsh/guides/services.md`  
**Machine:** home (Manjaro)  
**Authority:** @majkee  
**Status:** Active

---

## 📋 Services Overview

Your home machine runs several critical services. This guide covers monitoring, starting/stopping, and troubleshooting each.

### Active Services

| Service | Purpose | Port | Status Check |
|---------|---------|------|--------------|
| **nginx** | Web server | 80 | `systemctl status nginx` |
| **php74-fpm** | PHP 7.4 runtime (OpenCart) | socket | `systemctl status php74-fpm` |
| **php-fpm** | PHP 8.x runtime (Laravel) | socket | `systemctl status php-fpm` |
| **mariadb** | MySQL-compatible database | 3306 | `systemctl status mariadb` |
| **tailscale** | VPN tunnel | 41641 (UDP) | `systemctl status tailscaled` |
| **docker** | Container runtime | - | `systemctl status docker` |

---

## 🌐 nginx — Web Server

### Status Check
```bash
# Is it running?
systemctl status nginx

# What's listening on port 80?
sudo ss -tlnp | grep :80

# View access logs
sudo tail -f /var/log/nginx/access.log

# View error logs
sudo tail -f /var/log/nginx/error.log
```

### Service Management
```bash
# Start
sudo systemctl start nginx

# Stop
sudo systemctl stop nginx

# Restart (full restart, may have brief downtime)
sudo systemctl restart nginx

# Reload (graceful, no downtime)
sudo systemctl reload nginx

# Enable on boot
sudo systemctl enable nginx

# Disable on boot
sudo systemctl disable nginx
```

### Configuration
```bash
# Test config before applying
sudo nginx -t

# View parsed configuration
sudo nginx -T | less

# Sites available
ls /etc/nginx/sites-available/

# Sites enabled (active)
ls /etc/nginx/sites-enabled/

# Main config
sudo cat /etc/nginx/nginx.conf
```

### Common Issues & Fixes

**Port 80 already in use:**
```bash
sudo ss -tlnp | grep :80
# Kill the process or stop nginx
```

**502 Bad Gateway:**
```bash
# Check PHP-FPM is running
systemctl status php74-fpm php-fpm

# Check sockets exist
ls -la /run/php74-fpm/php-fpm.sock
ls -la /run/php-fpm/php-fpm.sock
```

**403 Forbidden:**
```bash
# Check file permissions
ls -la ~/www/your-site/

# Fix permissions
chmod 755 ~/www/your-site/
sudo chown -R http:http ~/www/your-site/storage
```

---

## 🐘 PHP-FPM — PHP Runtime

You have **two versions** running simultaneously:

### PHP 7.4 (OpenCart)
```bash
# Status
systemctl status php74-fpm

# Start/stop
sudo systemctl start php74-fpm
sudo systemctl stop php74-fpm
sudo systemctl restart php74-fpm

# Socket location
ls -la /run/php74-fpm/php-fpm.sock

# Config directory
ls /etc/php74/php-fpm.d/

# Logs
tail -f /var/log/php74-fpm.log
```

### PHP 8.x (Laravel)
```bash
# Status
systemctl status php-fpm

# Start/stop
sudo systemctl start php-fpm
sudo systemctl stop php-fpm
sudo systemctl restart php-fpm

# Socket location
ls -la /run/php-fpm/php-fpm.sock

# Config directory
ls /etc/php/php-fpm.d/

# Logs
tail -f /var/log/php-fpm.log
```

### Common Issues

**PHP not executing:**
```bash
# Check if FPM running
systemctl is-active php-fpm

# Check socket exists and is writable
ls -la /run/php-fpm/php-fpm.sock

# Check nginx config points to correct socket
grep fastcgi_pass /etc/nginx/sites-available/your-site
```

**Slow PHP execution:**
```bash
# Check PHP limits
php -i | grep -E "max_execution|memory_limit|upload_max"

# Edit PHP config (may need to restart)
sudo nano /etc/php/php.ini
# Or: /etc/php74/php.ini for PHP 7.4

# Restart FPM
sudo systemctl restart php-fpm
```

---

## 🗄️ MariaDB — Database

### Status Check
```bash
# Is it running?
systemctl status mariadb

# Can you connect?
mariadb -u majkee -p

# What databases exist?
mariadb -u majkee -p -e "SHOW DATABASES;"
```

### Service Management
```bash
# Start
sudo systemctl start mariadb

# Stop
sudo systemctl stop mariadb

# Restart
sudo systemctl restart mariadb

# Enable on boot
sudo systemctl enable mariadb

# Check logs
sudo journalctl -u mariadb -n 50
```

### Backup & Restore

**Backup:**
```bash
# Backup all databases
mysqldump -u majkee -p --all-databases > ~/backup-full.sql

# Backup single database
mysqldump -u majkee -p fantasyobchod > ~/backup-fo.sql
```

**Restore:**
```bash
# Restore all
mysql -u majkee -p < ~/backup-full.sql

# Restore single database
mysql -u majkee -p fantasyobchod < ~/backup-fo.sql
```

### Common Issues

**Connection refused:**
```bash
# Check if running
systemctl is-active mariadb

# Check socket exists
ls -la /var/run/mysqld/mysql.sock

# Start it
sudo systemctl start mariadb
```

**Database corrupted:**
```bash
# Repair table
mariadb -u majkee -p
REPAIR TABLE table_name;

# Or check entire database
mysqlcheck -u majkee -p --repair fantasyobchod
```

---

## 🔒 Tailscale — VPN

### Status Check
```bash
# Is running?
systemctl status tailscaled

# Current IP
tailscale ip -4

# Connected devices
tailscale peers

# Full status
tailscale status
```

### Service Management
```bash
# Connect/login
sudo tailscale up

# Disconnect
sudo tailscale down

# View status
systemctl status tailscaled

# Logs
journalctl -u tailscaled -n 50
```

### Troubleshooting

**Not connected:**
```bash
# Reconnect
sudo tailscale up

# Check daemon
systemctl restart tailscaled
```

**Can't reach other devices:**
```bash
# Check peers are visible
tailscale peers

# Check firewall (usually not an issue on home machine)
# But check: sudo firewall-cmd --list-all
```

---

## 🐳 Docker — Container Runtime

### Status Check
```bash
# Is daemon running?
systemctl status docker

# List containers
docker ps -a

# List images
docker images

# Disk usage
docker system df
```

### Service Management
```bash
# Start daemon
sudo systemctl start docker

# Stop all containers and daemon
sudo systemctl stop docker

# Restart
sudo systemctl restart docker

# Enable on boot
sudo systemctl enable docker

# Check user permissions
groups | grep docker
```

### Common Tasks

**Check if user can run Docker:**
```bash
docker ps
# If permission denied, user not in docker group:
sudo usermod -aG docker $USER
# Then logout/login to apply group change
```

**View logs:**
```bash
# System logs
sudo journalctl -u docker -n 50

# Container logs
docker logs container-name
```

---

## 🎯 Service Monitoring Substrate Functions

Add these to your monitoring toolkit:

```bash
# Add to ~/.config/zsh/archx/commands.zsh

substrate_services_status() {
    echo "[SUBSTRATE] Service Status Check:"
    echo ""
    for service in nginx php74-fpm php-fpm mariadb tailscaled docker; do
        local status=$(systemctl is-active $service 2>/dev/null || echo "not-installed")
        printf "%-20s: %s\n" "$service" "$status"
    done
}

substrate_services_check() {
    echo "[SUBSTRATE] Service Health Check:"
    echo ""
    
    # nginx
    echo -n "nginx: "
    systemctl is-active nginx > /dev/null && echo "✅" || echo "❌"
    
    # PHP-FPM
    echo -n "php74-fpm: "
    systemctl is-active php74-fpm > /dev/null && echo "✅" || echo "❌"
    
    echo -n "php-fpm: "
    systemctl is-active php-fpm > /dev/null && echo "✅" || echo "❌"
    
    # MariaDB
    echo -n "mariadb: "
    systemctl is-active mariadb > /dev/null && echo "✅" || echo "❌"
    
    # Tailscale
    echo -n "tailscaled: "
    systemctl is-active tailscaled > /dev/null && echo "✅" || echo "❌"
    
    # Docker
    echo -n "docker: "
    systemctl is-active docker > /dev/null && echo "✅" || echo "❌"
}

watch-services() {
    echo "[WATCH] Service status (Ctrl+C to stop):"
    watch -n 5 'systemctl status nginx php74-fpm php-fpm mariadb tailscaled docker | grep -E "Active|running"'
}
```

---

## 🚀 Service Startup Checklist

**When you boot or resume development:**

```bash
# 1. Check everything
sysmon

# 2. Verify services
substrate_services_check

# 3. Test web access
curl -I http://fantasyobchod.l
curl -I http://freya.l

# 4. Test database
mariadb -u majkee -p -e "SELECT 1;"

# 5. Check logs for errors
sudo tail -20 /var/log/nginx/error.log
```

---

## 📊 Service Dependencies

```
nginx
├── php74-fpm (for OpenCart)
│   └── /run/php74-fpm/php-fpm.sock
├── php-fpm (for Laravel)
│   └── /run/php-fpm/php-fpm.sock
└── Can run without database (static sites)

Laravel/OpenCart
├── nginx (web server)
├── PHP-FPM (runtime)
└── mariadb (database)

Tailscale
└── Independent (VPN connectivity only)

Docker
└── Independent (container runtime)
```

---

## 🔧 Quick Command Reference

```bash
# Check all service status
systemctl status nginx php74-fpm php-fpm mariadb tailscaled docker

# Restart all web services
sudo systemctl restart nginx php74-fpm php-fpm

# View all error logs
sudo tail -f /var/log/nginx/error.log

# Test nginx config
sudo nginx -t

# Quick database check
mariadb -u majkee -p -e "SHOW DATABASES;"

# Check port usage
sudo ss -tlnp
```

---

**Last Updated:** 2026-06-29  
**Next Review:** When adding new services or projects
