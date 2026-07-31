# OpenCart @home Setup - Complete Guide
**Machine:** Manjaro KDE Plasma  
**Project:** FantasyObchod (OpenCart PHP 7.4)  
**Date:** March 5-6, 2026  
**Author:** @majkee + @Houston  
**Purpose:** External memory - complete documentation of nginx + PHP-FPM setup

---

## 📋 TABLE OF CONTENTS

1. [Initial State Assessment](#1-initial-state-assessment)
2. [PHP 7.4 Installation](#2-php-74-installation)
3. [nginx Installation & Configuration](#3-nginx-installation--configuration)
4. [Error Resolution Journey](#4-error-resolution-journey)
5. [Missing PHP Extensions](#5-missing-php-extensions)
6. [vendor/ Directory Restoration](#6-vendor-directory-restoration)
6. [ALTERNATIVE: Running Composer with Docker](#6-working-composer-docker)
7. [Tracy Debugger Directories](#7-tracy-debugger-directories)
8. [Custom Sessions Directory](#8-custom-sessions-directory)
9. [Final Working Configuration](#9-final-working-configuration)
10. [Educational Insights](#10-educational-insights)
11. [Future Reference](#11-future-reference)

---

## 1. INITIAL STATE ASSESSMENT

### What Was Already Done (February 2026)

**Before this session:**
- ✅ Manjaro KDE reinstalled (fresh system)
- ✅ MariaDB installed and running
- ✅ Database `fantasyobchod` physically restored from backup
- ✅ Project files at `/home/hruzam/www/fantasyobchod/`
- ✅ config.php and admin/config.php exist (in Git)

### What Was Missing

```bash
# Check system state
pacman -Q | grep php
# Output: php 8.5.3-1, php-fpm 8.5.3-1

pacman -Q | grep nginx
# Output: (nothing - not installed)
```

**Missing:**
- ❌ nginx web server
- ❌ PHP 7.4 (only PHP 8.5.3 installed)
- ❌ PHP 7.4 FPM
- ❌ PHP 7.4 extensions
- ❌ vendor/ directory
- ❌ Log directories (tracy/)
- ❌ Custom session directory

---

## 2. PHP 7.4 INSTALLATION

### Why PHP 7.4 Specifically?

**OpenCart requirement:** PHP 7.4 (not compatible with PHP 8.5)

```bash
# From composer.lock in project:
"php": ">=5.6.0,<8.0.0"  ← Packages require PHP < 8.0
```

### Installation Commands

```bash
# Install PHP 7.4 from AUR
yay -S php74 php74-fpm

# Install essential OpenCart extensions
yay -S php74-gd php74-intl php74-mbstring php74-xml php74-zip php74-curl

# Verify installation
pacman -Q | grep php74
```

**Result:**
```
php74 7.4.33-11
php74-fpm 7.4.33-11
php74-curl 7.4.33-11
php74-gd 7.4.33-11
php74-intl 7.4.33-11
php74-mbstring 7.4.33-11
php74-xml 7.4.33-11
php74-zip 7.4.33-11
```

### Start PHP-FPM Service

```bash
sudo systemctl enable php74-fpm
sudo systemctl start php74-fpm
systemctl status php74-fpm
```

### 🎓 EDUCATIONAL: What is PHP-FPM?

**PHP-FPM** = PHP FastCGI Process Manager

```
nginx (web server)
    ↓ forwards PHP requests via socket
PHP-FPM (PHP processor)
    ↓ executes PHP code
Returns HTML to nginx
    ↓ serves to browser
```

**Why not just PHP CLI?**
- FPM is optimized for web serving
- Manages multiple worker processes
- Better performance for concurrent requests
- Persistent processes (don't restart for each request)

---

## 3. NGINX INSTALLATION & CONFIGURATION

### Install nginx

```bash
sudo pacman -S nginx
```

### Create Directory Structure

```bash
# Manjaro doesn't create these by default (Debian/Ubuntu style)
sudo mkdir -p /etc/nginx/sites-available
sudo mkdir -p /etc/nginx/sites-enabled
```

**Why this structure?**
- `sites-available/` = All site configs (inactive)
- `sites-enabled/` = Symlinks to active sites only
- Easy to enable/disable sites without deleting configs

### Configure Main nginx.conf

```bash
sudo nano /etc/nginx/nginx.conf
```

**Add inside `http {}` block:**
```nginx
http {
    include /etc/nginx/sites-enabled/*;  # ← Add this line
    # ... rest of config
}
```

### Create FantasyObchod Site Config

```bash
sudo nano /etc/nginx/sites-available/fantasyobchod
```

**Initial configuration:**
```nginx
server {
    listen 80;
    server_name fantasyobchod.l;
    root /home/hruzam/www/fantasyobchod;

    index index.php index.html;
    charset utf-8;

    error_log /var/log/nginx/fantasyobchod-error.log;
    access_log /var/log/nginx/fantasyobchod-access.log;

    # Main routing for OpenCart
    location / {
        try_files $uri $uri/ /index.php?$args;
    }

    # Admin panel
    location /admin {
        index index.php;
        try_files $uri $uri/ /admin/index.php?$args;
    }

    # PHP via FPM 7.4
    location ~ \.php$ {
        try_files $uri =404;
        fastcgi_pass unix:/run/php74-fpm/php-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }

    # Security
    location ~ /\. {
        deny all;
    }
    
    location ~* ^/system/ {
        deny all;
    }

    # Static files
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 30d;
        access_log off;
    }
}
```

### Enable Site

```bash
# Create symlink to enable site
sudo ln -s /etc/nginx/sites-available/fantasyobchod /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Enable and start nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```

### Add Domain to /etc/hosts

```bash
echo "127.0.0.1   fantasyobchod.l" | sudo tee -a /etc/hosts
```

---

## 4. ERROR RESOLUTION JOURNEY

**This section documents the progression of errors and fixes**

### Error 1: 403 Forbidden

**Test:**
```bash
curl -I http://fantasyobchod.l
# Output: HTTP/1.1 403 Forbidden
```

**Diagnosis:**
```bash
sudo tail /var/log/nginx/fantasyobchod-error.log
# stat() "/home/hruzam/www/fantasyobchod/" failed (13: Permission denied)
```

**Root cause:** nginx running as user `hruzam` but couldn't access files

**Fix #1: Change nginx user**
```bash
sudo nano /etc/nginx/nginx.conf
```
Change:
```nginx
#user http;  # ← Was commented
user hruzam;  # ← Set to hruzam
```

**Fix #2: Socket permissions**
```bash
sudo nano /etc/php74/php-fpm.d/www.conf
```
Change:
```ini
listen.owner = hruzam  # ← Was: http
listen.group = hruzam  # ← Was: http
```

```bash
sudo systemctl restart php74-fpm
sudo systemctl reload nginx
curl -I http://fantasyobchod.l
# Output: HTTP/1.1 502 Bad Gateway  ← Progress!
```

### Error 2: 502 Bad Gateway

**Meaning:** nginx found files but can't talk to PHP-FPM

**Diagnosis:**
```bash
sudo tail /var/log/nginx/fantasyobchod-error.log
# connect() to unix:/run/php74-fpm/php-fpm.sock failed (13: Permission denied)
```

**Root cause:** Socket path worked, but ownership fixed the issue in previous step

**Test:**
```bash
curl -I http://fantasyobchod.l
# Output: HTTP/1.1 404 Not Found
# X-Powered-By: PHP/7.4.33  ← PHP IS WORKING!
```

### Error 3: 404 Not Found (PHP Working)

**Meaning:** PHP executes but OpenCart returns 404

**Diagnosis:**
```bash
sudo tail /var/log/nginx/fantasyobchod-error.log
# FastCGI sent in stderr: "Primary script unknown"
```

**Root cause:** PHP-FPM couldn't access `/home/hruzam/` directory

**Check permissions:**
```bash
ls -ld /home/hruzam
# drwx------ (700) ← Only owner can access!
```

**The Critical Fix:**
```bash
chmod 711 /home/hruzam
```

**Test:**
```bash
curl -I http://fantasyobchod.l
# Output: HTTP/1.1 200 OK  ← SUCCESS!
# X-Powered-By: PHP/7.4.33
```

### 🎓 EDUCATIONAL: Why chmod 711?

**Permission breakdown:**
```
chmod 711 = drwx--x--x
            │││  │  │
            │││  │  └─ Others (PHP-FPM user 'http'): Execute only
            │││  └──── Group: Execute only
            │└┴──────── Owner (you): Full access
```

**What this allows:**
```
✅ PHP-FPM can TRAVERSE through /home/hruzam/
✅ PHP-FPM can reach /home/hruzam/www/fantasyobchod/
❌ PHP-FPM CANNOT list /home/hruzam/ contents
❌ PHP-FPM CANNOT read /home/hruzam/Documents/
❌ PHP-FPM CANNOT access /home/hruzam/.ssh/
```

**Security:**
- **711** = Most secure for web serving from home directory
- **755** = Less secure (allows listing directory contents)
- **700** = Most secure but breaks web server access

**The principle:** Execute permission allows **passing through** but not **reading contents**

---

## 5. MISSING PHP EXTENSIONS

### Error: JsonSerializable Interface Not Found

**Browser showed:**
```
Fatal error: Interface 'JsonSerializable' not found
in /home/hruzam/www/fantasyobchod/vendor/illuminate/collections/Enumerable.php
```

**Root cause:** PHP 7.4 JSON extension missing

**Fix:**
```bash
yay -S php74-json
sudo systemctl restart php74-fpm
```

### Error: mysqli Interface Not Found

**Root cause:** MySQL driver missing

**Search for correct package:**
```bash
yay -Ss php74 | grep -i mysql
# aur/php74-mysql 7.4.33-11  ← Found it!
```

**Fix:**
```bash
yay -S php74-mysql
sudo systemctl restart php74-fpm
```

**Verify all extensions:**
```bash
pacman -Q | grep php74
```

**Complete list:**
```
php74
php74-fpm
php74-curl
php74-gd
php74-iconv
php74-intl
php74-json      ← Added
php74-mbstring
php74-mysql     ← Added (includes mysqli)
php74-soap
php74-xml
php74-zip
```

### 🎓 EDUCATIONAL: Why These Extensions?

| Extension | Purpose | OpenCart Uses For |
|-----------|---------|------------------|
| **mysqli** | MySQL database connection | All database operations |
| **json** | JSON encoding/decoding | API responses, data serialization |
| **gd** | Image manipulation | Product images, thumbnails |
| **intl** | Internationalization | Multi-language, currencies |
| **mbstring** | Multi-byte strings | UTF-8 text handling |
| **xml** | XML processing | Feeds, imports/exports |
| **curl** | HTTP requests | External APIs, payment gateways |
| **zip** | Compression | Backups, extensions |

---

## 6. VENDOR/ DIRECTORY RESTORATION

### Why vendor/ Was Missing

**Check .gitignore:**
```bash
cat .gitignore | grep vendor
# /vendor  ← Excluded from Git
```

**Why?**
- vendor/ contains 1000+ dependency files
- Generated by `composer install`
- Different per PHP version
- Git only tracks composer.json/composer.lock

### Problem: No PHP 7.4 CLI Binary

**Attempted:**
```bash
php74 composer install
# Output: php74 is a shell function, not binary!
```

**Discovery:**
```bash
which php74
# php74: aliased to php74_on  ← Just a function to switch FPM!

ls /usr/bin/php*
# /usr/bin/php-fpm74  ← Only FPM, no CLI!
```

**Why composer failed:**
```
composer needs PHP CLI binary
    ↓
php74 AUR package only provides PHP-FPM
    ↓
No way to run `composer install` with PHP 7.4
```

### Solution: Restore from Backup

```bash
# Check backup location
ls -la /mnt/manjaro_data/BackupReinstalling/

# Copy vendor/ directory from backup
cp -r /path/to/backup/vendor /home/hruzam/www/fantasyobchod/

# Verify
ls -la /home/hruzam/www/fantasyobchod/vendor/autoload.php
```

### 🎓 EDUCATIONAL: vendor/ Structure

```
vendor/
├── autoload.php           ← Composer's class autoloader
├── composer/              ← Composer metadata
├── illuminate/            ← Laravel Collections
├── tracy/                 ← Tracy Debugger
├── google/                ← Google API Client
└── [many more packages]
```

**Why it's needed:**
```
index.php loads:
    ↓
require 'vendor/autoload.php'
    ↓
Autoloader makes all packages available
    ↓
Without it: Fatal error on every PHP class
```
---

## 6.5 ALTERNATIVE: Running Composer with Docker

### The Problem Revisited

**From Section 6:** AUR's `php74` package only provides PHP-FPM (FastCGI Process Manager), not the CLI (Command Line Interface) binary needed for composer.

```
php74 package contents:
✅ php-fpm74        ← Works with nginx (web server)
❌ php74 CLI binary ← Missing! Needed for composer
```

**Original solution:** Copy `vendor/` from backup

**Better long-term solution:** Use Docker for portable, clean composer execution

---

## ✅ Docker Solution Benefits

| Benefit | Why It Matters |
|---------|---------------|
| **Portable** | Same setup @home and @office |
| **No system pollution** | Doesn't conflict with system PHP 8 |
| **Version flexibility** | Easy to switch PHP versions per project |
| **Production-like** | Matches deployment environment |
| **Future-proof** | Works for all projects (OpenCart + Laravel) |
| **Clean** | No complex PHP compilation from source |

---

## 🚀 Docker Setup (One-Time)

### Step 1: Install Docker

```bash
# Install Docker
sudo pacman -S docker

# Enable and start service
sudo systemctl enable --now docker

# Verify installation
systemctl status docker
# Should show: active (running)
```

### Step 2: Add User to Docker Group

```bash
# Add yourself to docker group
sudo usermod -aG docker $USER

# Verify group added
groups | grep docker
# If empty, group not applied yet
```

### Step 3: Apply Group Membership

**You MUST logout and login** for group membership to take effect!

```bash
# Option A: Logout/login (recommended)
# Close terminal, logout from desktop, login again

# Option B: Temporary for current session only
newgrp docker
```

### Step 4: Test Docker

```bash
# Test Docker works
docker run hello-world

# Should show: "Hello from Docker!" message
```

---

## 🔧 Create Composer Wrapper Scripts

### For PHP 7.4 Projects (OpenCart)

```bash
# Create directory if it doesn't exist
mkdir -p ~/.local/bin

# Create composer74 script
nano ~/.local/bin/composer74
```

**Paste this:**
```bash
#!/bin/bash
# Composer with PHP 7.4 via Docker
docker run --rm -it \
  -v "$(pwd)":/app \
  -v "$HOME/.composer:/tmp/composer" \
  -u $(id -u):$(id -g) \
  composer:2 \
  --ignore-platform-req=ext-posix \
  --ignore-platform-req=ext-pcntl \
  "$@"
```

**Make executable:**
```bash
chmod +x ~/.local/bin/composer74
```

### For PHP 8+ Projects (Laravel)

```bash
# Create composer8 script
nano ~/.local/bin/composer8
```

**Paste this:**
```bash
#!/bin/bash
# Composer with PHP 8+ via Docker
docker run --rm -it \
  -v "$(pwd)":/app \
  -v "$HOME/.composer:/tmp/composer" \
  -u $(id -u):$(id -g) \
  composer:latest \
  "$@"
```

**Make executable:**
```bash
chmod +x ~/.local/bin/composer8
```

---

## 🎯 Usage

### Basic Commands

```bash
# OpenCart project (PHP 7.4)
cd ~/www/fantasyobchod
composer74 install
composer74 update
composer74 require vendor/package

# Laravel project (PHP 8+)
cd ~/www/freya
composer8 install
composer8 update
```

### How It Works

```
composer74 install
    ↓
Runs Docker container with PHP 7.4
    ↓
Mounts current directory to /app in container
    ↓
Runs composer inside container
    ↓
Writes vendor/ to your actual project directory
    ↓
Container stops automatically (--rm flag)
```

**Key flags explained:**
- `--rm` = Remove container after execution (no cleanup needed)
- `-it` = Interactive terminal (see output in real-time)
- `-v "$(pwd)":/app` = Mount current directory as /app in container
- `-v "$HOME/.composer:/tmp/composer"` = Cache composer packages
- `-u $(id -u):$(id -g)` = Run as your user (files owned by you, not root)
- `--ignore-platform-req=ext-posix` = Skip POSIX extension check (not needed)

---

## 🔍 Troubleshooting

### Error: Permission Denied (Docker Socket)

```bash
# Check Docker service running
systemctl status docker

# Check user in docker group
groups | grep docker

# If not in group:
sudo usermod -aG docker $USER
# Then LOGOUT and LOGIN
```

### Error: Cannot Connect to Docker Daemon

```bash
# Start Docker service
sudo systemctl start docker

# Enable for auto-start
sudo systemctl enable docker
```

### Composer Downloads Are Slow

**First run will be slow** (downloading container image):
```
[*] Pulling composer:2 image... (~200MB)
```

**Subsequent runs are fast** (uses cached image).

**Speed up subsequent installs:**
```bash
# Composer caches packages in ~/.composer/
# This persists between Docker runs
ls -la ~/.composer/cache/
```

---

## 📊 Comparison: Backup vs Docker

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| **Copy vendor/ from backup** | Instant, works immediately | Need backup available, no updates possible | Quick setup, emergency recovery |
| **Docker composer** | Can install/update any time, portable, clean | First-time setup, requires internet | Long-term development, updates needed |

**Recommendation:** Use BOTH!
1. Copy vendor/ from backup initially (get working fast)
2. Set up Docker for future updates/new packages

---

## 🔄 Updating OpenCart Dependencies

**When you need to add a new package:**

```bash
cd ~/www/fantasyobchod

# Add new package
composer74 require vendor/new-package

# Update existing packages
composer74 update

# Regenerate autoloader
composer74 dump-autoload -o
```

**After updates:**
```bash
# Restart PHP-FPM to clear opcache
sudo systemctl restart php74-fpm
```

---

## 🎓 Educational: Why Docker Works

**The core issue:**
```
System PHP = 8.5.3 (default)
OpenCart needs PHP < 8.0
php74 package = Only FPM, no CLI
```

**Docker solution:**
```
Container = Isolated environment with PHP 7.4 CLI
    ↓
Your project files mounted into container
    ↓
Composer runs with correct PHP version
    ↓
Writes to your actual project (not container)
    ↓
Container removed (clean!)
```

**Why this is better than building PHP 7.4 from source:**
- No manual compilation
- No system conflicts
- Easy to remove (just delete script)
- Matches production environment
- Reproducible across machines

---

## 🔐 Security Considerations

**Is running Docker as user safe?**

✅ YES - The `-u $(id -u):$(id -g)` flag ensures:
- Container runs as YOUR user (not root)
- Files created are owned by YOU
- No privilege escalation

**Docker group membership:**
- Allows socket access (`/var/run/docker.sock`)
- Container still runs as your user
- No root access inside container

**What Docker CAN'T do (security boundaries):**
- Can't modify system files (only project directory mounted)
- Can't access other users' files
- Can't bypass file permissions
- Container isolated from host system

---

## 📋 Quick Reference Card

```bash
# ==================================================
# DOCKER COMPOSER QUICK REFERENCE (@home)
# ==================================================

# SETUP (one-time):
sudo pacman -S docker
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
# LOGOUT/LOGIN to apply

# CREATE SCRIPTS:
~/.local/bin/composer74  # PHP 7.4 (OpenCart)
~/.local/bin/composer8   # PHP 8+ (Laravel)

# USAGE:
cd ~/www/fantasyobchod
composer74 install       # Install dependencies
composer74 update        # Update packages
composer74 require X     # Add package

cd ~/www/freya
composer8 install        # Laravel with PHP 8+

# TROUBLESHOOT:
systemctl status docker  # Check service
groups | grep docker     # Check group
docker run hello-world   # Test Docker

# ==================================================
```

---

## 🔗 Integration with Existing Guide

**This Docker solution complements Section 6** without replacing it:

```
Section 6: vendor/ Directory Restoration
    ├── 6.1-6.4: Original backup solution ✅
    └── 6.5: Docker alternative (this section) ✅

Use backup method:
- Initial setup (fast)
- Emergency recovery
- When Docker not available

Use Docker method:
- Adding new packages
- Updating dependencies
- Long-term development
```

---

## ✅ Verification Checklist

After Docker setup, verify:

```bash
# Docker installed and running
□ systemctl status docker → active (running)

# User in docker group
□ groups | grep docker → shows "docker"

# Docker accessible
□ docker run hello-world → Success message

# Composer scripts exist and executable
□ ls -la ~/.local/bin/composer74 → shows -rwxr-xr-x
□ ls -la ~/.local/bin/composer8  → shows -rwxr-xr-x

# Scripts work
□ composer74 --version → Composer version 2.x.x
□ composer8 --version  → Composer version 2.x.x

# Can install packages
□ cd ~/www/fantasyobchod && composer74 install → Success
```

**If all checked ✅ → Docker composer fully functional!**

---

## 7. TRACY DEBUGGER DIRECTORIES

### Error: Tracy Logging Directory Not Found

**Browser showed:**
```
RuntimeException: Logging directory '/home/hruzam/www/fantasyobchod/tracy/log' is not found.
```

**Root cause:** Tracy debugger needs log directory (gitignored)

**Check .gitignore:**
```bash
grep tracy .gitignore
# /admin/tracy/log
# /tracy/log
```

### Solution

**Create frontend Tracy directory:**
```bash
mkdir -p /home/hruzam/www/fantasyobchod/tracy/log
sudo chown -R http:http /home/hruzam/www/fantasyobchod/tracy/
```

**Create admin Tracy directory:**
```bash
mkdir -p /home/hruzam/www/fantasyobchod/admin/tracy/log
sudo chown -R http:http /home/hruzam/www/fantasyobchod/admin/tracy/
```

**Why `chown http:http`?**
```
PHP-FPM runs as user 'http'
    ↓
Tracy tries to write log files
    ↓
Needs write permission
    ↓
Solution: Make 'http' user the owner
```

### 🎓 EDUCATIONAL: Tracy Debugger

**What Tracy does:**
```php
// In index.php:
Debugger::enable(Debugger::DEVELOPMENT, __DIR__ . '/tracy/log');
```

**Functions:**
- Logs PHP errors, warnings, exceptions
- Creates detailed HTML error pages
- Stores in tracy/log/ directory
- Essential for development debugging

**File ownership for web apps:**
```
Source code → owned by developer (hruzam)
Log/cache directories → owned by web server (http)
Upload directories → owned by web server (http)
```

---

## 8. CUSTOM SESSIONS DIRECTORY

### Error: Admin Login Stuck

**Symptom:** Login form submits but redirects back to login

**Diagnosis:**
```bash
# Check what sessions are created
ls -la /var/lib/php74/sessions/
# Only: tracy-* files, NO sess_* files!
```

**Test session creation:**
```bash
echo '<?php session_start(); echo session_id(); ?>' > test-session.php
firefox http://fantasyobchod.l/test-session.php
# Shows session ID!

ls -la /var/lib/php74/sessions/
# sess_0mies4114e9mld6g7bb5q7upm6 created ✅
```

**Conclusion:** PHP sessions work, but OpenCart uses custom path!

### Root Cause Discovery

**Check OpenCart session library:**
```bash
cat /home/hruzam/www/fantasyobchod/system/library/session.php
```

**Found:**
```php
/* Q-mod -- session extend */
ini_set('session.save_path','/home/hruzam/www/sessions/');
```

**OpenCart uses custom session directory!**

### Solution

```bash
# Create custom session directory
mkdir -p /home/hruzam/www/sessions

# Make writable by PHP-FPM
sudo chown http:http /home/hruzam/www/sessions
sudo chmod 700 /home/hruzam/www/sessions

# Verify
ls -ld /home/hruzam/www/sessions
# drwx------ 2 http http ... /home/hruzam/www/sessions
```

**Test admin login:**
```bash
firefox http://fantasyobchod.l/admin/
# Admin panel loads! ✅
```

### 🎓 EDUCATIONAL: Session Storage

**Default PHP sessions:**
```
session.save_path = /var/lib/php74/sessions/
```

**OpenCart custom sessions:**
```
session.save_path = /home/hruzam/www/sessions/
```

**Why custom path?**
- Longer session lifetime (33 days vs default)
- Project-specific session storage
- Easier backup with project files

**Why chmod 700 (not 711)?**
```
700 = drwx------
      │││
      │││ Nobody else can access AT ALL
      │└┴─ Read/write/execute only by owner (http)
      └─── Owner: http (PHP-FPM user)
```

**Sessions contain sensitive data:**
- User credentials
- Authentication tokens
- Shopping cart contents
- Personal information

**Security principle:** Most restrictive permissions that still work

---

## 9. FINAL WORKING CONFIGURATION

### Complete File Structure

```
/home/hruzam/www/fantasyobchod/
├── admin/
│   ├── config.php          ← DB credentials, paths
│   ├── tracy/
│   │   └── log/            ← Owned by http:http
│   └── ...
├── catalog/
├── system/
│   ├── library/
│   │   └── session.php     ← Custom session path
│   ├── storage/            ← Owned by http:http
│   └── cache/              ← Owned by http:http
├── vendor/                 ← Restored from backup
│   └── autoload.php
├── tracy/
│   └── log/                ← Owned by http:http
├── config.php              ← DB credentials, paths
└── index.php

/home/hruzam/www/sessions/  ← Custom session directory
                              ← Owned by http:http

/var/lib/php74/sessions/    ← Default PHP sessions
                              ← Owned by http:http
```

### nginx Configuration

**File:** `/etc/nginx/sites-available/fantasyobchod`

```nginx
server {
    listen 80;
    server_name fantasyobchod.l;
    root /home/hruzam/www/fantasyobchod;

    index index.php index.html;
    charset utf-8;

    error_log /var/log/nginx/fantasyobchod-error.log;
    access_log /var/log/nginx/fantasyobchod-access.log;

    location / {
        try_files $uri $uri/ /index.php?$args;
    }

    location /admin {
        index index.php;
        try_files $uri $uri/ /admin/index.php?$args;
    }

    location ~ \.php$ {
        try_files $uri =404;
        fastcgi_pass unix:/run/php74-fpm/php-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }

    location ~ /\. {
        deny all;
    }
    
    location ~* ^/system/ {
        deny all;
    }

    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 30d;
        access_log off;
    }
}
```

### PHP-FPM Configuration

**File:** `/etc/php74/php-fpm.d/www.conf`

**Critical settings:**
```ini
user = http
group = http
listen = /run/php74-fpm/php-fpm.sock
listen.owner = hruzam
listen.group = hruzam
listen.mode = 0660
```

### Permission Summary

```bash
# Home directory (allow traversal)
chmod 711 /home/hruzam

# Project files (owned by you)
chown -R hruzam:hruzam /home/hruzam/www/fantasyobchod/

# Writable directories (owned by web server)
sudo chown -R http:http /home/hruzam/www/fantasyobchod/tracy/
sudo chown -R http:http /home/hruzam/www/fantasyobchod/admin/tracy/
sudo chown -R http:http /home/hruzam/www/fantasyobchod/system/storage/
sudo chown -R http:http /home/hruzam/www/fantasyobchod/system/cache/
sudo chown -R http:http /home/hruzam/www/sessions/

# Session directories (700 - most secure)
chmod 700 /home/hruzam/www/sessions/
chmod 700 /var/lib/php74/sessions/

# Log directories (755 - owner writable)
chmod -R 755 /home/hruzam/www/fantasyobchod/tracy/
chmod -R 755 /home/hruzam/www/fantasyobchod/admin/tracy/
```

### Service Status

```bash
# Check all services running
systemctl status nginx
systemctl status php74-fpm
systemctl status mariadb

# All should show: active (running)
```

### Final Test

```bash
# Frontend
curl -I http://fantasyobchod.l
# HTTP/1.1 200 OK
# X-Powered-By: PHP/7.4.33

firefox http://fantasyobchod.l
# OpenCart shop loads with products ✅

# Admin
firefox http://fantasyobchod.l/admin/
# Admin login works ✅
# Admin panel accessible ✅
```

---

## 10. EDUCATIONAL INSIGHTS

### The Error Progression Pattern

**Understanding the journey:**
```
403 Forbidden
    ↓ nginx can't access files
    ↓ Fixed: nginx user permissions
502 Bad Gateway
    ↓ nginx → PHP-FPM communication broken
    ↓ Fixed: socket permissions
404 Not Found (PHP working)
    ↓ PHP-FPM can't traverse /home/hruzam/
    ↓ Fixed: chmod 711 /home/hruzam
200 OK (but errors)
    ↓ Missing PHP extensions
    ↓ Fixed: install php74-json, php74-mysql
200 OK (but Tracy errors)
    ↓ Missing log directories
    ↓ Fixed: create tracy/log, admin/tracy/log
200 OK (frontend works, admin stuck)
    ↓ Custom session directory missing
    ↓ Fixed: create /home/hruzam/www/sessions/
FULLY WORKING ✅
```

**Key lesson:** Each error brings you closer. Every fix reveals the next layer.

### Permission Patterns for Web Apps

| Directory Type | Owner | Permissions | Why |
|----------------|-------|-------------|-----|
| **Home directory** | user | 711 | Allow traversal only |
| **Source code** | user | 755 | Developer owns, web server reads |
| **Log directories** | http | 755 | Web server writes logs |
| **Session directories** | http | 700 | Private data, web server only |
| **Cache directories** | http | 755 | Web server writes cache |
| **Upload directories** | http | 755 | Web server writes uploads |

### nginx → PHP-FPM Communication

**Socket-based communication:**
```
nginx (user: hruzam)
    ↓ writes to socket
unix:/run/php74-fpm/php-fpm.sock (owner: hruzam)
    ↓ PHP-FPM reads from socket
PHP-FPM (user: http)
    ↓ executes PHP code
    ↓ needs to read project files
Project files (owner: hruzam, permissions: 755)
```

**Why socket permissions matter:**
- Socket must be readable by nginx user
- Socket must be writable by PHP-FPM user
- Solution: `listen.owner = hruzam` allows nginx to write
- `user = http` allows PHP-FPM to read project files

### Composer & vendor/ Dependency

**The dependency chain:**
```
composer.json
    ↓ defines
Required packages & versions
    ↓ composer reads
composer.lock
    ↓ exact versions locked
composer install
    ↓ downloads & installs
vendor/ directory
    ↓ contains
All PHP dependencies
    ↓ loaded by
vendor/autoload.php
```

**Why composer install needs matching PHP version:**
```
Packages specify: "php": ">=7.2,<8.0"
    ↓
Composer checks: php --version
    ↓
If PHP 8.5: "Your PHP version (8.5.3) does not satisfy"
    ↓
If PHP 7.4: Installs successfully
```

---

## 11. FUTURE REFERENCE

### Quick Troubleshooting Commands

```bash
# Check service status
systemctl status nginx
systemctl status php74-fpm
systemctl status mariadb

# View recent nginx errors
sudo tail -30 /var/log/nginx/fantasyobchod-error.log

# View PHP-FPM logs
sudo journalctl -u php74-fpm -n 50 --no-pager

# Test nginx config
sudo nginx -t

# Restart services
sudo systemctl restart php74-fpm
sudo systemctl reload nginx

# Check PHP sessions
sudo ls -la /var/lib/php74/sessions/
sudo ls -la /home/hruzam/www/sessions/

# Check permissions
ls -ld /home/hruzam
ls -ld /home/hruzam/www/fantasyobchod
ls -ld /home/hruzam/www/sessions

# Test database connection
mariadb -u majkee -p fantasyobchod -e "SELECT 'OK' as test;"
```

### Common Issues & Solutions

| Problem | Diagnostic Command | Solution |
|---------|-------------------|----------|
| **403 Forbidden** | `ls -ld /home/hruzam` | `chmod 711 /home/hruzam` |
| **502 Bad Gateway** | `systemctl status php74-fpm` | Check PHP-FPM running, socket permissions |
| **Primary script unknown** | `ls -ld /home/hruzam` | `chmod 711 /home/hruzam` |
| **Tracy log error** | `ls -la tracy/log` | `sudo chown -R http:http tracy/` |
| **Session not persisting** | `ls -ld /home/hruzam/www/sessions` | Check custom session dir exists, owned by http |
| **JsonSerializable error** | `pacman -Q \| grep php74-json` | `yay -S php74-json` |
| **Database connection fails** | `systemctl status mariadb` | Check MariaDB running, credentials correct |

### Setting Up Laravel Projects (Freya, PSDVS)

**For PHP 8+ Laravel projects:**

```bash
# Copy nginx template for Laravel
sudo cp /etc/nginx/sites-available/fantasyobchod /etc/nginx/sites-available/freya

# Edit for Laravel
sudo nano /etc/nginx/sites-available/freya
```

**Changes needed:**
```nginx
server_name freya.l;
root /home/hruzam/www/freya/public;  # ← Note /public for Laravel!
fastcgi_pass unix:/run/php-fpm/php-fpm.sock;  # ← PHP 8+ socket
```

**Enable and test:**
```bash
sudo ln -s /etc/nginx/sites-available/freya /etc/nginx/sites-enabled/
echo "127.0.0.1   freya.l" | sudo tee -a /etc/hosts
sudo nginx -t && sudo systemctl reload nginx
```

### If You Reinstall or Setup New Machine

**Checklist:**
1. ✅ Install MariaDB, restore database
2. ✅ Install PHP 7.4 + extensions (see section 2)
3. ✅ Install nginx
4. ✅ Create nginx config (copy from this guide)
5. ✅ Set home directory permissions: `chmod 711 /home/hruzam`
6. ✅ Configure PHP-FPM socket permissions
7. ✅ Restore vendor/ from backup
8. ✅ Create tracy/log directories
9. ✅ Create custom sessions directory
10. ✅ Set ownership: `sudo chown -R http:http` for writable dirs

**Time estimate:** ~45 minutes with this guide (vs 5+ hours without!)

---

## 📚 APPENDIX: Complete Command Reference

### Initial Setup (One-Time)

```bash
# Install PHP 7.4
yay -S php74 php74-fpm php74-gd php74-intl php74-mbstring \
       php74-xml php74-zip php74-curl php74-json php74-mysql \
       php74-soap php74-iconv

# Install nginx
sudo pacman -S nginx

# Create nginx directories
sudo mkdir -p /etc/nginx/sites-{available,enabled}

# Start services
sudo systemctl enable --now php74-fpm
sudo systemctl enable --now nginx
sudo systemctl enable --now mariadb
```

### Configuration Files

**nginx main config:**
```bash
sudo nano /etc/nginx/nginx.conf
# Add: include /etc/nginx/sites-enabled/*;
```

**PHP-FPM pool config:**
```bash
sudo nano /etc/php74/php-fpm.d/www.conf
# Set: listen.owner = hruzam
# Set: listen.group = hruzam
```

**nginx site config:**
```bash
sudo nano /etc/nginx/sites-available/fantasyobchod
# Paste config from section 9
```

### Permission Setup

```bash
# Home directory
chmod 711 /home/hruzam

# Create writable directories
mkdir -p /home/hruzam/www/fantasyobchod/tracy/log
mkdir -p /home/hruzam/www/fantasyobchod/admin/tracy/log
mkdir -p /home/hruzam/www/sessions

# Set ownership
sudo chown -R http:http /home/hruzam/www/fantasyobchod/tracy/
sudo chown -R http:http /home/hruzam/www/fantasyobchod/admin/tracy/
sudo chown -R http:http /home/hruzam/www/fantasyobchod/system/storage/
sudo chown -R http:http /home/hruzam/www/fantasyobchod/system/cache/
sudo chown -R http:http /home/hruzam/www/sessions/

# Set permissions
chmod 700 /home/hruzam/www/sessions/
chmod 700 /var/lib/php74/sessions/
```

### Enable Site & Test

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/fantasyobchod /etc/nginx/sites-enabled/

# Add domain
echo "127.0.0.1   fantasyobchod.l" | sudo tee -a /etc/hosts

# Test config
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx

# Test
curl -I http://fantasyobchod.l
firefox http://fantasyobchod.l
```

---

## 🎓 KEY TAKEAWAYS

1. **Permissions matter** - `chmod 711` on home directory was critical
2. **Socket paths vary** - Always check actual socket location
3. **PHP-FPM ownership** - Socket owner must match nginx user
4. **Extensions required** - json, mysql/mysqli essential for OpenCart
5. **vendor/ not in Git** - Must be restored or regenerated
6. **Custom paths** - Check session.php for custom session directory
7. **Writable dirs need ownership** - Tracy, sessions, cache → owned by http
8. **Error progression teaches** - Each error reveals next layer
9. **Documentation saves time** - This guide = your external memory
10. **Testing incrementally** - Fix one issue, test, move to next

---

## ✅ VERIFICATION CHECKLIST

After following this guide, verify:

```bash
# Services running
□ systemctl status nginx → active (running)
□ systemctl status php74-fpm → active (running)
□ systemctl status mariadb → active (running)

# PHP version
□ curl -I http://fantasyobchod.l | grep "X-Powered-By: PHP/7.4"

# Extensions installed
□ pacman -Q | grep php74 → 11+ packages

# Directories exist with correct ownership
□ ls -ld /home/hruzam → drwx--x--x (711)
□ ls -ld /home/hruzam/www/sessions → drwx------ http http (700)
□ ls -ld /home/hruzam/www/fantasyobchod/tracy/log → http http
□ ls -ld /home/hruzam/www/fantasyobchod/admin/tracy/log → http http

# vendor/ exists
□ ls -la /home/hruzam/www/fantasyobchod/vendor/autoload.php

# Sites work
□ curl -I http://fantasyobchod.l → HTTP/1.1 200 OK
□ firefox http://fantasyobchod.l → OpenCart loads
□ firefox http://fantasyobchod.l/admin/ → Admin login works
```

**If all checked ✅ → Setup complete!**

---

## 📝 NOTES FROM @MAJKEE

*Incorporated from installationPHP_mH.MD*

**Most crucial discovery:** 
```bash
chmod 711 /home/hruzam  # THIS ONE IS MOST CRUCIAL
```

**Socket path difference noticed:**
```bash
# Expected: /run/php-fpm74/php-fpm.sock
# Actual: /run/php74-fpm/php-fpm.sock
```

**Package search method that worked:**
```bash
yay -Ss php74 | grep -i mysql
# Found: aur/php74-mysql 7.4.33-11
```

---

**END OF GUIDE**

*This document is your external memory. When you need to setup OpenCart again (new machine, reinstall, helping colleague), start here. Everything you need is documented with context and explanations.*

*Last updated: March 6, 2026*  
*Status: Complete and verified working*  
*Next project: Laravel (Freya, PSDVS) using similar approach*
