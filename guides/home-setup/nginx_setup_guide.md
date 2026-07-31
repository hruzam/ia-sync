# nginx + PHP-FPM Setup Guide (@home machine)
**Purpose:** Complete reference for setting up multi-PHP web server environment  
**Context:** Manjaro KDE, dual PHP (7.4 for OpenCart, 8+ for Laravel)  
**Author:** Majkee + Houston  
**Created:** 2026-02-28  
**Status:** Active reference for @home machine

---

## WHY THIS GUIDE EXISTS

**Problem:** You don't configure nginx every day. When you need it (new project, reinstall), you've forgotten details.  
**Solution:** This document is your external memory - copy/paste ready, with explanations.

---

## TABLE OF CONTENTS

1. [Initial Setup (One-time)](#1-initial-setup-one-time)
2. [Understanding nginx Basics](#2-understanding-nginx-basics)
3. [Template System (Your Time-Saver)](#3-template-system-your-time-saver)
4. [FantasyObchod Configuration](#4-fantasyobchod-configuration)
5. [Laravel Projects (Freya/PSDVS)](#5-laravel-projects-freyapsdvs)
6. [PHP Version Switching](#6-php-version-switching)
7. [Troubleshooting](#7-troubleshooting)
8. [Quick Reference](#8-quick-reference)

---

## 1. INITIAL SETUP (One-time)

### 1.1 Install nginx
```bash
sudo pacman -S nginx
```

**What this does:** Installs nginx web server (like Apache but faster, more efficient).

### 1.2 Create sites-enabled structure (like Debian/Ubuntu)
```bash
# Manjaro doesn't create this by default, so we add it
sudo mkdir -p /etc/nginx/sites-available
sudo mkdir -p /etc/nginx/sites-enabled
sudo mkdir -p /etc/nginx/templates
```

**Why?**  
- `sites-available/` = All site configs (inactive)
- `sites-enabled/` = Symlinks to active sites (like aliases)
- `templates/` = Reusable templates (your time-saver)

### 1.3 Edit main nginx config
```bash
sudo nano /etc/nginx/nginx.conf
```

**Add this line** inside the `http {}` block (around line 30):
```nginx
http {
    # ... existing config ...
    
    include /etc/nginx/sites-enabled/*;  # ← Add this line
    
    # ... rest of config ...
}
```

**What this does:** Tells nginx to load all configs from sites-enabled/ directory.

### 1.4 Test and enable nginx
```bash
# Test configuration (always do this before reloading!)
sudo nginx -t

# Expected output:
# nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
# nginx: configuration file /etc/nginx/nginx.conf test is successful

# Enable nginx to start on boot
sudo systemctl enable nginx

# Start nginx now
sudo systemctl start nginx

# Check status
systemctl status nginx
```

**What nginx -t does:** Checks config for syntax errors before reloading (prevents breaking live sites).

---

## 2. UNDERSTANDING NGINX BASICS

### 2.1 How nginx processes requests

```
User types: http://fantasyobchod.l
    ↓
nginx checks: server_name fantasyobchod.l
    ↓
nginx finds: root /home/hruzam/www/fantasyobchod
    ↓
nginx tries: index.php (for PHP apps)
    ↓
nginx passes to: PHP-FPM via socket
    ↓
PHP-FPM executes: index.php
    ↓
Returns HTML to: user's browser
```

### 2.2 Key nginx directives explained

| Directive | What it does | Example |
|-----------|--------------|---------|
| `server_name` | Domain to respond to | `server_name fantasyobchod.l;` |
| `root` | Project directory | `root /home/hruzam/www/fantasyobchod;` |
| `index` | Default file to serve | `index index.php index.html;` |
| `location` | Rules for URL patterns | `location / { ... }` |
| `try_files` | Try files in order | `try_files $uri $uri/ /index.php;` |
| `fastcgi_pass` | Where PHP-FPM listens | `fastcgi_pass unix:/run/php-fpm74/php-fpm.sock;` |

### 2.3 Socket vs TCP for PHP-FPM

**Socket (faster, recommended):**
```nginx
fastcgi_pass unix:/run/php-fpm74/php-fpm.sock;
```

**TCP (slower, but easier to debug):**
```nginx
fastcgi_pass 127.0.0.1:9000;
```

We'll use **sockets** for production, TCP for troubleshooting.

---

## 3. TEMPLATE SYSTEM (Your Time-Saver)

### 3.1 Why templates?

**Without templates:** Copy-paste entire config, edit 5 places, miss one, debug for 30 minutes.  
**With templates:** Copy template, edit 3 lines, done in 2 minutes.

### 3.2 Create OpenCart template (PHP 7.4)

```bash
sudo nano /etc/nginx/templates/opencart-php74.conf
```

**Paste this:**
```nginx
# OpenCart (PHP 7.4) Template
# Copy to: /etc/nginx/sites-available/yourproject
# Edit: server_name, root, error_log/access_log paths

server {
    listen 80;
    server_name PROJECT_DOMAIN;  # ← EDIT THIS
    root PROJECT_PATH;            # ← EDIT THIS

    index index.php index.html;
    charset utf-8;

    # Logging (helps debugging)
    error_log /var/log/nginx/PROJECT_NAME-error.log;    # ← EDIT THIS
    access_log /var/log/nginx/PROJECT_NAME-access.log;  # ← EDIT THIS

    # OpenCart SEO URLs
    location = /sitemap.xml {
        try_files $uri @opencart;
    }
    
    location = /googlebase.xml {
        try_files $uri @opencart;
    }
    
    location / {
        try_files $uri @opencart;
    }
    
    location @opencart {
        rewrite ^/(.+)$ /index.php?_route_=$1 last;
    }

    # Admin panel
    location /admin {
        index index.php;
        try_files $uri $uri/ /admin/index.php?$args;
    }

    # PHP processing via PHP-FPM 7.4
    location ~ \.php$ {
        try_files $uri =404;
        fastcgi_pass unix:/run/php-fpm74/php-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
        
        # OpenCart needs these
        fastcgi_param HTTP_MOD_REWRITE On;
    }

    # Security: deny access to sensitive files
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
    
    location ~* ^/system/ {
        deny all;
    }
    
    location ~ /composer\.(json|lock) {
        deny all;
    }

    # Static files optimization
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        expires 30d;
        access_log off;
        add_header Cache-Control "public, immutable";
    }
}
```

**Save and exit:** `Ctrl+O`, `Enter`, `Ctrl+X`

### 3.3 Create Laravel template (PHP 8+)

```bash
sudo nano /etc/nginx/templates/laravel-php8.conf
```

**Paste this:**
```nginx
# Laravel (PHP 8+) Template
# Copy to: /etc/nginx/sites-available/yourproject
# Edit: server_name, root, error_log/access_log paths

server {
    listen 80;
    server_name PROJECT_DOMAIN;     # ← EDIT THIS
    root PROJECT_PATH/public;       # ← EDIT THIS (note /public!)

    index index.php index.html;
    charset utf-8;

    # Logging
    error_log /var/log/nginx/PROJECT_NAME-error.log;    # ← EDIT THIS
    access_log /var/log/nginx/PROJECT_NAME-access.log;  # ← EDIT THIS

    # Laravel routing
    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    # PHP processing via PHP-FPM 8+
    location ~ \.php$ {
        try_files $uri =404;
        fastcgi_pass unix:/run/php-fpm/php-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
        include fastcgi_params;
    }

    # Security: deny access to hidden files
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }

    # Deny access to Laravel config
    location ~ /\.env {
        deny all;
    }
    
    location ~ /composer\.(json|lock) {
        deny all;
    }

    # Static files optimization
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        expires 30d;
        access_log off;
        add_header Cache-Control "public, immutable";
    }
}
```

**Save and exit:** `Ctrl+O`, `Enter`, `Ctrl+X`

---

## 4. FANTASYOBCHOD CONFIGURATION

### 4.1 Create config from template

```bash
# Copy template
sudo cp /etc/nginx/templates/opencart-php74.conf /etc/nginx/sites-available/fantasyobchod

# Edit the copy
sudo nano /etc/nginx/sites-available/fantasyobchod
```

### 4.2 Edit these 5 lines

**Find and replace:**
```nginx
# Line ~6
server_name PROJECT_DOMAIN;
# Change to:
server_name fantasyobchod.l;

# Line ~7
root PROJECT_PATH;
# Change to:
root /home/hruzam/www/fantasyobchod;

# Line ~12-13
error_log /var/log/nginx/PROJECT_NAME-error.log;
access_log /var/log/nginx/PROJECT_NAME-access.log;
# Change to:
error_log /var/log/nginx/fantasyobchod-error.log;
access_log /var/log/nginx/fantasyobchod-access.log;
```

**Save:** `Ctrl+O`, `Enter`, `Ctrl+X`

### 4.3 Enable site and reload

```bash
# Create symlink (this "enables" the site)
sudo ln -s /etc/nginx/sites-available/fantasyobchod /etc/nginx/sites-enabled/

# Test config (ALWAYS do this!)
sudo nginx -t

# If OK, reload nginx
sudo systemctl reload nginx
```

### 4.4 Add to /etc/hosts

```bash
sudo nano /etc/hosts
```

**Add this line:**
```
127.0.0.1   fantasyobchod.l
```

**Save:** `Ctrl+O`, `Enter`, `Ctrl+X`

### 4.5 Test in browser

```bash
# Start PHP-FPM 7.4 first (if not running)
sudo systemctl start php74-fpm

# Check status
systemctl status php74-fpm

# Open browser
firefox http://fantasyobchod.l
```

**Expected:** OpenCart loads!

---

## 5. LARAVEL PROJECTS (Freya/PSDVS)

### 5.1 Freya/Imago setup

```bash
# Copy Laravel template
sudo cp /etc/nginx/templates/laravel-php8.conf /etc/nginx/sites-available/freya

# Edit
sudo nano /etc/nginx/sites-available/freya
```

**Change these lines:**
```nginx
server_name freya.l;
root /home/hruzam/www/freya/public;  # ← Note /public!
error_log /var/log/nginx/freya-error.log;
access_log /var/log/nginx/freya-access.log;
```

**Enable:**
```bash
sudo ln -s /etc/nginx/sites-available/freya /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

**Add to /etc/hosts:**
```bash
sudo nano /etc/hosts
# Add: 127.0.0.1   freya.l
```

### 5.2 PSDVS setup (same process)

```bash
sudo cp /etc/nginx/templates/laravel-php8.conf /etc/nginx/sites-available/psdvs
sudo nano /etc/nginx/sites-available/psdvs
```

**Change:**
```nginx
server_name psdvs.l;
root /home/hruzam/www/PSDVS/public;
error_log /var/log/nginx/psdvs-error.log;
access_log /var/log/nginx/psdvs-access.log;
```

**Enable:**
```bash
sudo ln -s /etc/nginx/sites-available/psdvs /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
echo "127.0.0.1   psdvs.l" | sudo tee -a /etc/hosts
```

---

## 6. PHP VERSION SWITCHING

### 6.1 Global switching (affects CLI)

```bash
# Already defined in your project-switcher.zsh:
php74    # Switches to PHP 7.4
php8     # Switches to PHP 8+
phpst    # Shows status
```

### 6.2 Per-site switching (nginx)

**To switch FantasyObchod to PHP 8 (for testing):**
```bash
sudo nano /etc/nginx/sites-available/fantasyobchod
```

**Change this line:**
```nginx
# From:
fastcgi_pass unix:/run/php-fpm74/php-fpm.sock;

# To:
fastcgi_pass unix:/run/php-fpm/php-fpm.sock;
```

**Reload:**
```bash
sudo nginx -t && sudo systemctl reload nginx

# Switch FPM services
sudo systemctl stop php74-fpm
sudo systemctl start php-fpm
```

### 6.3 Check which PHP-FPM is running

```bash
# Your existing phpst command shows this:
phpst

# Or check services directly:
systemctl status php74-fpm
systemctl status php-fpm
```

---

## 7. TROUBLESHOOTING

### 7.1 Site not loading - Checklist

```bash
# 1. Is nginx running?
systemctl status nginx

# 2. Is PHP-FPM running?
systemctl status php74-fpm   # for OpenCart
systemctl status php-fpm     # for Laravel

# 3. Is domain in /etc/hosts?
cat /etc/hosts | grep fantasyobchod

# 4. Is site enabled?
ls -la /etc/nginx/sites-enabled/ | grep fantasyobchod

# 5. Any nginx errors?
sudo tail -f /var/log/nginx/fantasyobchod-error.log

# 6. Test nginx config
sudo nginx -t
```

### 7.2 Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| `502 Bad Gateway` | PHP-FPM not running | `sudo systemctl start php74-fpm` |
| `404 Not Found` | Wrong root path | Check `root` in nginx config |
| `File not found` | Missing index.php | Check project files exist |
| `Permission denied` | Wrong file ownership | `sudo chown -R hruzam:hruzam ~/www/fantasyobchod` |
| `Connection refused` | nginx not running | `sudo systemctl start nginx` |

### 7.3 View logs in real-time

```bash
# All nginx errors
sudo tail -f /var/log/nginx/error.log

# Specific site errors
sudo tail -f /var/log/nginx/fantasyobchod-error.log

# PHP-FPM errors
sudo journalctl -fu php74-fpm
```

### 7.4 Reset everything

```bash
# Stop all services
sudo systemctl stop nginx php74-fpm php-fpm

# Restart in order
sudo systemctl start php74-fpm
sudo systemctl start php-fpm
sudo systemctl start nginx

# Check all running
systemctl status nginx php74-fpm php-fpm
```

---

## 8. QUICK REFERENCE

### 8.1 Daily commands

```bash
# Reload nginx after config change
sudo nginx -t && sudo systemctl reload nginx

# Restart PHP-FPM after changes
sudo systemctl restart php74-fpm

# View errors
sudo tail -f /var/log/nginx/fantasyobchod-error.log

# Test specific URL
curl -I http://fantasyobchod.l
```

### 8.2 New project in 2 minutes

```bash
# 1. Copy template
sudo cp /etc/nginx/templates/opencart-php74.conf /etc/nginx/sites-available/newproject

# 2. Edit 5 lines (server_name, root, logs)
sudo nano /etc/nginx/sites-available/newproject

# 3. Enable site
sudo ln -s /etc/nginx/sites-available/newproject /etc/nginx/sites-enabled/

# 4. Test and reload
sudo nginx -t && sudo systemctl reload nginx

# 5. Add to hosts
echo "127.0.0.1   newproject.l" | sudo tee -a /etc/hosts

# Done!
```

### 8.3 File locations

```bash
# nginx main config
/etc/nginx/nginx.conf

# Site configs (inactive)
/etc/nginx/sites-available/

# Active sites (symlinks)
/etc/nginx/sites-enabled/

# Templates (your library)
/etc/nginx/templates/

# Logs
/var/log/nginx/

# PHP-FPM configs
/etc/php74/php-fpm.d/
/etc/php/php-fpm.d/
```

### 8.4 Integration with your toolkit

Your `fo-toolkit.zsh` already has:
```bash
fo -adm    # Opens Adminer (needs nginx running!)
```

After nginx setup, this will work at: `http://fantasyobchod.l/adminer`

---

## 9. NEXT STEPS

### 9.1 After this guide

1. ✅ nginx installed and configured
2. ✅ Templates created for future projects
3. ✅ FantasyObchod running locally
4. ⏭️ Import database (MariaDB setup)
5. ⏭️ Configure OpenCart config.php
6. ⏭️ Test admin panel
7. ⏭️ Setup Laravel projects (Freya, PSDVS)

### 9.2 Save this guide

```bash
# Recommended location:
~/www/PSDVS/env/nginx_setup_guide.md

# Or in your project documentation:
~/Documents/dev-guides/nginx_setup_guide.md
```

---

## 10. EDUCATIONAL NOTES

### 10.1 What you learned

- **nginx architecture:** How web servers route requests
- **FastCGI:** How nginx talks to PHP
- **Socket communication:** Unix sockets vs TCP
- **Virtual hosts:** Multiple sites on one server
- **Template patterns:** Reusable configurations
- **Service management:** systemctl commands
- **Log analysis:** Debugging with error logs

### 10.2 Transferable skills

This knowledge applies to:
- Production servers (Linux VPS, AWS, DigitalOcean)
- Docker containers (nginx containers)
- Client projects (deploying Laravel/OpenCart)
- Performance tuning (nginx optimization)

### 10.3 Why not Valet?

**Valet:** Abstraction layer (hides nginx/PHP details)  
**Manual nginx:** Direct control, understanding, troubleshooting

You chose manual nginx because:
1. ✅ Understand how it works (your learning style)
2. ✅ Direct troubleshooting (no abstraction layer)
3. ✅ Production-ready knowledge (industry standard)
4. ✅ Flexibility (custom configs per project)

**Time investment:** 30 minutes initial learning → Lifetime knowledge

---

## CONCLUSION

You now have:
1. ✅ Complete nginx setup for multi-PHP environment
2. ✅ Template system for 2-minute project setups
3. ✅ Troubleshooting guide for common issues
4. ✅ Educational context (why each step matters)

**This document is your external memory.** When you reinstall or add a project, come back here. Copy-paste the commands, understand the why, move forward.

**Questions?** Check section 7 (Troubleshooting) or your logs.

---

*Last updated: 2026-02-28*  
*Machine: @home (Manjaro KDE)*  
*Author: Majkee + Houston*
