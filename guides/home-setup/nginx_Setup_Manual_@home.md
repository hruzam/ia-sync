# nginx Setup Manual - @home Machine
**Complete guide for OpenCart + Laravel configurations**  
**Machine:** Manjaro KDE Plasma  
**Last Updated:** March 7, 2026

---

## 📋 TABLE OF CONTENTS

1. [Current Setup Overview](#current-setup)
2. [Directory Structure](#directory-structure)
3. [FantasyObchod (OpenCart) Configuration](#fantasyobchod-opencart)
4. [Laravel Configuration (Freya/PSDVS)](#laravel-configuration)
5. [Virtual Host Management](#virtual-host-management)
6. [PHP-FPM Integration](#php-fpm-integration)
7. [Common Patterns](#common-patterns)
8. [Troubleshooting](#troubleshooting)
9. [Commands Reference](#commands-reference)

---

## 🎯 CURRENT SETUP OVERVIEW {#current-setup}

### What's Running

```
nginx (Web Server)
    ↓ Routes by domain
    ├─ fantasyobchod.l → PHP 7.4 FPM → OpenCart
    ├─ freya.l → PHP 8 FPM → Laravel (to be configured)
    ├─ psdvs.l → PHP 8 FPM → Laravel (to be configured)
    └─ laravel-training.l → PHP 8 FPM → Laravel training project (planned)

/etc/hosts:
127.0.0.1  fantasyobchod.l
127.0.0.1  freya.l
127.0.0.1  psdvs.l
127.0.0.1  laravel-training.l
```

### Services

```bash
# nginx
systemctl status nginx
# Running on: port 80

# PHP-FPM 7.4 (OpenCart)
systemctl status php74-fpm
# Socket: /run/php74-fpm/php-fpm.sock

# PHP-FPM 8.x (Laravel)
systemctl status php-fpm
# Socket: /run/php-fpm/php-fpm.sock
```

---

## 📂 DIRECTORY STRUCTURE {#directory-structure}

### nginx Configuration

```
/etc/nginx/
├── nginx.conf                  ← Main config (global settings)
├── sites-available/            ← Virtual host configs (all sites)
│   ├── fantasyobchod          ← OpenCart config
│   ├── freya                  ← Laravel config (to create)
│   ├── psdvs                  ← Laravel config (to create)
│   └── laravel-training       ← Laravel training config (to create)
└── sites-enabled/              ← Active sites (symlinks)
    ├── fantasyobchod -> ../sites-available/fantasyobchod
    ├── freya -> ../sites-available/freya
    ├── psdvs -> ../sites-available/psdvs
    └── laravel-training -> ../sites-available/laravel-training

/var/log/nginx/                 ← Log files
├── access.log                  ← All access logs
├── error.log                   ← All error logs
├── fantasyobchod-access.log   ← Site-specific access
├── fantasyobchod-error.log    ← Site-specific errors
├── freya-error.log
└── psdvs-error.log
```

### Project Files

```
~/www/
├── fantasyobchod/              ← OpenCart (PHP 7.4)
│   ├── index.php              ← Front controller
│   ├── admin/                 ← Admin panel
│   └── system/
├── freya/                      ← Laravel (PHP 8)
│   ├── public/                ← Web root (important!)
│   │   └── index.php          ← Front controller
│   ├── app/
│   ├── routes/
│   └── artisan
├── PSDVS/                      ← Laravel (PHP 8)
│   ├── public/                ← Web root (important!)
│   │   └── index.php
│   ├── app/
│   └── artisan
└── Laravel-training-project/   ← Laravel training project (PHP 8)
    ├── public/                ← Web root (important!)
    │   └── index.php
    ├── app/
    ├── routes/
    └── artisan
```

---

## 🛒 FANTASYOBCHOD (OPENCART) {#fantasyobchod-opencart}

### Configuration File

**Location:** `/etc/nginx/sites-available/fantasyobchod`

```nginx
server {
    listen 80;
    server_name fantasyobchod.l;
    
    # Document root (project root, NOT public/)
    root /home/hruzam/www/fantasyobchod;
    
    # Default file
    index index.php index.html;
    
    # Character encoding
    charset utf-8;
    
    # Logging
    error_log /var/log/nginx/fantasyobchod-error.log;
    access_log /var/log/nginx/fantasyobchod-access.log;
    
    # Main location (frontend)
    location / {
        try_files $uri $uri/ /index.php?$args;
    }
    
    # Admin panel
    location /admin {
        index index.php;
        try_files $uri $uri/ /admin/index.php?$args;
    }
    
    # PHP handler
    location ~ \.php$ {
        try_files $uri =404;
        
        # PHP-FPM 7.4 socket
        fastcgi_pass unix:/run/php74-fpm/php-fpm.sock;
        
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
        
        # Timeouts
        fastcgi_read_timeout 300;
        fastcgi_send_timeout 300;
    }
    
    # Security: Deny access to hidden files
    location ~ /\. {
        deny all;
    }
    
    # Security: Protect system directory
    location ~* ^/system/ {
        deny all;
    }
    
    # Static files caching
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        expires 30d;
        access_log off;
    }
}
```

### Key Features

**OpenCart-Specific:**
- ✅ Root is project directory (not public/)
- ✅ Separate admin location block
- ✅ System directory protection
- ✅ Static file caching
- ✅ PHP 7.4 FPM integration

### Enable Site

```bash
# Create symlink
sudo ln -sf /etc/nginx/sites-available/fantasyobchod /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload
sudo systemctl reload nginx
```

---

## 🔶 LARAVEL CONFIGURATION {#laravel-configuration}

### Freya Configuration

**Location:** `/etc/nginx/sites-available/freya`

```nginx
server {
    listen 80;
    server_name freya.l;
    
    # IMPORTANT: Laravel uses public/ subdirectory
    root /home/hruzam/www/freya/public;
    
    # Default file
    index index.php index.html;
    
    # Character encoding
    charset utf-8;
    
    # Logging
    error_log /var/log/nginx/freya-error.log;
    access_log /var/log/nginx/freya-access.log;
    
    # Client body size (for file uploads)
    client_max_body_size 100M;
    
    # Main location (Laravel routing)
    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }
    
    # PHP handler
    location ~ \.php$ {
        try_files $uri =404;
        
        # PHP-FPM 8.x socket
        fastcgi_pass unix:/run/php-fpm/php-fpm.sock;
        
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
        include fastcgi_params;
        
        # Laravel specific
        fastcgi_param PATH_INFO $fastcgi_path_info;
        fastcgi_param SCRIPT_NAME $fastcgi_script_name;
        
        # Timeouts
        fastcgi_read_timeout 300;
        fastcgi_send_timeout 300;
    }
    
    # Security: Deny access to hidden files
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
    
    # Security: Deny access to sensitive files
    location ~ /\.(?:htaccess|htpasswd|env) {
        deny all;
    }
    
    # Static files caching
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }
    
    # Favicon
    location = /favicon.ico {
        access_log off;
        log_not_found off;
    }
    
    # Robots
    location = /robots.txt {
        access_log off;
        log_not_found off;
    }
}
```

### PSDVS Configuration

**Location:** `/etc/nginx/sites-available/psdvs`

```nginx
server {
    listen 80;
    server_name psdvs.l;
    
    # IMPORTANT: Laravel uses public/ subdirectory
    root /home/hruzam/www/PSDVS/public;
    
    # Default file
    index index.php index.html;
    
    # Character encoding
    charset utf-8;
    
    # Logging
    error_log /var/log/nginx/psdvs-error.log;
    access_log /var/log/nginx/psdvs-access.log;
    
    # Client body size
    client_max_body_size 100M;
    
    # Main location (Laravel routing)
    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }
    
    # PHP handler
    location ~ \.php$ {
        try_files $uri =404;
        
        # PHP-FPM 8.x socket
        fastcgi_pass unix:/run/php-fpm/php-fpm.sock;
        
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
        include fastcgi_params;
        
        # Laravel specific
        fastcgi_param PATH_INFO $fastcgi_path_info;
        fastcgi_param SCRIPT_NAME $fastcgi_script_name;
        
        # Timeouts
        fastcgi_read_timeout 300;
        fastcgi_send_timeout 300;
    }
    
    # Security: Deny access to hidden files
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
    
    # Security: Deny access to sensitive files
    location ~ /\.(?:htaccess|htpasswd|env) {
        deny all;
    }
    
    # Static files caching
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }
    
    # Favicon
    location = /favicon.ico {
        access_log off;
        log_not_found off;
    }
    
    # Robots
    location = /robots.txt {
        access_log off;
        log_not_found off;
    }
}
```

### Laravel Key Differences from OpenCart

| Feature | OpenCart | Laravel |
|---------|----------|---------|
| **Root** | Project directory | `public/` subdirectory |
| **Routing** | `try_files $uri $uri/ /index.php?$args` | `try_files $uri $uri/ /index.php?$query_string` |
| **PHP-FPM** | PHP 7.4 socket | PHP 8.x socket |
| **Admin** | Separate location block | Built into routing |
| **.env Protection** | N/A | Deny access to .env |

---

## 🔧 VIRTUAL HOST MANAGEMENT {#virtual-host-management}

### Create New Site

```bash
# 1. Create configuration
sudo nano /etc/nginx/sites-available/newsite

# 2. Enable site (create symlink)
sudo ln -sf /etc/nginx/sites-available/newsite /etc/nginx/sites-enabled/

# 3. Add to /etc/hosts
echo "127.0.0.1  newsite.l" | sudo tee -a /etc/hosts

# 4. Test configuration
sudo nginx -t

# 5. Reload nginx
sudo systemctl reload nginx

# 6. Test in browser
firefox http://newsite.l
```

### Disable Site

```bash
# Remove symlink (keeps config for later)
sudo rm /etc/nginx/sites-enabled/sitename

# Reload nginx
sudo systemctl reload nginx
```

### Edit Site

```bash
# Edit configuration
sudo nano /etc/nginx/sites-available/sitename

# Test
sudo nginx -t

# Apply changes
sudo systemctl reload nginx
```

### List Sites

```bash
# Available sites
ls -la /etc/nginx/sites-available/

# Enabled sites
ls -la /etc/nginx/sites-enabled/
```

---

## 🔌 PHP-FPM INTEGRATION {#php-fpm-integration}

### Socket vs TCP

**Current Setup: Unix Sockets (Faster)**

```nginx
# PHP 7.4 (OpenCart)
fastcgi_pass unix:/run/php74-fpm/php-fpm.sock;

# PHP 8.x (Laravel)
fastcgi_pass unix:/run/php-fpm/php-fpm.sock;
```

**Alternative: TCP (if sockets don't work)**

```nginx
# PHP 7.4
fastcgi_pass 127.0.0.1:9074;

# PHP 8.x
fastcgi_pass 127.0.0.1:9000;
```

### Verify Socket Exists

```bash
# Check PHP 7.4 socket
ls -la /run/php74-fpm/php-fpm.sock
# Should exist and be writable

# Check PHP 8.x socket
ls -la /run/php-fpm/php-fpm.sock
# Should exist and be writable

# Check permissions
# Owner should match nginx config!
```

### Socket Permissions

**From PHP-FPM config** (`/etc/php74/php-fpm.d/www.conf`):

```ini
; Socket settings
listen = /run/php74-fpm/php-fpm.sock
listen.owner = hruzam
listen.group = hruzam
listen.mode = 0660

; Process settings
user = http
group = http
```

**Key Point:** Socket owner = your user, Process runs as `http`

---

## 🎨 COMMON PATTERNS {#common-patterns}

### Pattern 1: Simple PHP Site

```nginx
server {
    listen 80;
    server_name example.l;
    root /home/hruzam/www/example;
    index index.php;
    
    location / {
        try_files $uri $uri/ /index.php?$args;
    }
    
    location ~ \.php$ {
        fastcgi_pass unix:/run/php-fpm/php-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
```

### Pattern 2: Static HTML Site

```nginx
server {
    listen 80;
    server_name static.l;
    root /home/hruzam/www/static;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
```

### Pattern 3: Reverse Proxy (Node.js, etc.)

```nginx
server {
    listen 80;
    server_name app.l;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### Pattern 4: Multiple PHP Versions on Same Server

```nginx
# PHP 7.4 site
server {
    listen 80;
    server_name php74site.l;
    root /home/hruzam/www/php74site;
    
    location ~ \.php$ {
        fastcgi_pass unix:/run/php74-fpm/php-fpm.sock;
        include fastcgi_params;
    }
}

# PHP 8.x site
server {
    listen 80;
    server_name php8site.l;
    root /home/hruzam/www/php8site;
    
    location ~ \.php$ {
        fastcgi_pass unix:/run/php-fpm/php-fpm.sock;
        include fastcgi_params;
    }
}
```

---

## 🚨 TROUBLESHOOTING {#troubleshooting}

### Error: 502 Bad Gateway

**Cause:** PHP-FPM not running or socket issue

**Diagnose:**
```bash
# Check FPM running
systemctl status php74-fpm
systemctl status php-fpm

# Check socket exists
ls -la /run/php74-fpm/php-fpm.sock
ls -la /run/php-fpm/php-fpm.sock

# Check nginx error log
sudo tail -f /var/log/nginx/error.log
```

**Fix:**
```bash
# Start FPM
sudo systemctl start php74-fpm
sudo systemctl start php-fpm

# Check socket permissions in /etc/php74/php-fpm.d/www.conf
# listen.owner and listen.group should match nginx user
```

### Error: 403 Forbidden

**Cause:** Permission issues

**Diagnose:**
```bash
# Check file permissions
ls -la ~/www/fantasyobchod/

# Check home directory permissions
ls -ld /home/hruzam
# Should be: drwx--x--x (711)

# Check nginx error log
sudo tail -f /var/log/nginx/fantasyobchod-error.log
```

**Fix:**
```bash
# Fix home directory permissions (CRITICAL!)
chmod 711 /home/hruzam

# Fix project permissions
sudo chown -R hruzam:hruzam ~/www/fantasyobchod/
chmod -R 755 ~/www/fantasyobchod/

# Fix writable directories
sudo chown -R http:http ~/www/fantasyobchod/system/storage/
sudo chown -R http:http ~/www/fantasyobchod/system/cache/
```

### Error: 404 Not Found

**Cause:** Incorrect root or try_files directive

**Diagnose:**
```bash
# Check root path in config
grep "root" /etc/nginx/sites-available/sitename

# For Laravel, verify public/ exists
ls -la ~/www/freya/public/index.php

# Check nginx error log
sudo tail -f /var/log/nginx/freya-error.log
```

**Fix:**
```bash
# OpenCart: root should be project directory
root /home/hruzam/www/fantasyobchod;

# Laravel: root should be public/ subdirectory
root /home/hruzam/www/freya/public;
```

### Error: File downloads instead of executing

**Cause:** PHP-FPM not handling .php files

**Diagnose:**
```bash
# Check PHP location block exists
grep "\.php$" /etc/nginx/sites-available/sitename

# Check FPM running
systemctl status php-fpm
```

**Fix:**
```bash
# Ensure location ~ \.php$ block exists
# Ensure fastcgi_pass points to correct socket
# Restart FPM
sudo systemctl restart php-fpm
sudo systemctl reload nginx
```

### Error: Changes not reflecting

**Cause:** nginx config not reloaded

**Fix:**
```bash
# Test configuration first
sudo nginx -t

# If OK, reload
sudo systemctl reload nginx

# Or restart
sudo systemctl restart nginx

# Also clear browser cache
Ctrl + Shift + R
```

---

## 📋 COMMANDS REFERENCE {#commands-reference}

### Service Management

```bash
# nginx
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx
sudo systemctl reload nginx    # ← Preferred (no downtime)
sudo systemctl status nginx

# PHP-FPM 7.4
sudo systemctl start php74-fpm
sudo systemctl stop php74-fpm
sudo systemctl restart php74-fpm
sudo systemctl status php74-fpm

# PHP-FPM 8.x
sudo systemctl start php-fpm
sudo systemctl stop php-fpm
sudo systemctl restart php-fpm
sudo systemctl status php-fpm
```

### Configuration Testing

```bash
# Test nginx config (DO THIS BEFORE RELOAD!)
sudo nginx -t

# Test with verbose output
sudo nginx -T

# Show parsed configuration
sudo nginx -T | less
```

### Log Viewing

```bash
# nginx error log (all sites)
sudo tail -f /var/log/nginx/error.log

# Site-specific error log
sudo tail -f /var/log/nginx/fantasyobchod-error.log
sudo tail -f /var/log/nginx/freya-error.log

# Access log
sudo tail -f /var/log/nginx/access.log

# Search logs for errors
sudo grep "error" /var/log/nginx/fantasyobchod-error.log
sudo grep "404" /var/log/nginx/access.log
```

### Quick Diagnostics

```bash
# What's listening on port 80?
sudo netstat -tlnp | grep :80
# Should show: nginx

# Which sites are enabled?
ls -la /etc/nginx/sites-enabled/

# Check socket permissions
ls -la /run/php74-fpm/php-fpm.sock
ls -la /run/php-fpm/php-fpm.sock

# Test site response
curl -I http://fantasyobchod.l
curl -I http://freya.l
```

---

## 🚀 SETUP CHECKLIST (New Laravel Site)

**Example: Setting up Freya**

```bash
# Step 1: Create nginx config
sudo nano /etc/nginx/sites-available/freya
# Paste Laravel config from above

# Step 2: Enable site
sudo ln -sf /etc/nginx/sites-available/freya /etc/nginx/sites-enabled/

# Step 3: Add to /etc/hosts
echo "127.0.0.1  freya.l" | sudo tee -a /etc/hosts

# Step 4: Set Laravel permissions
cd ~/www/freya
chmod -R 755 storage bootstrap/cache
sudo chown -R http:http storage bootstrap/cache

# Step 5: Test nginx config
sudo nginx -t

# Step 6: Reload nginx
sudo systemctl reload nginx

# Step 7: Ensure PHP 8 FPM running
sudo systemctl start php-fpm
systemctl status php-fpm

# Step 8: Test in browser
firefox http://freya.l

# Step 9: Check logs if issues
sudo tail -f /var/log/nginx/freya-error.log
```

---

## 📝 CONFIGURATION TEMPLATES

### Quick Copy-Paste: Laravel Site

```bash
# Replace SITENAME and PATH
sudo tee /etc/nginx/sites-available/SITENAME << 'EOF'
server {
    listen 80;
    server_name SITENAME.l;
    root /home/hruzam/www/SITENAME/public;
    index index.php;
    charset utf-8;
    
    error_log /var/log/nginx/SITENAME-error.log;
    access_log /var/log/nginx/SITENAME-access.log;
    
    client_max_body_size 100M;
    
    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }
    
    location ~ \.php$ {
        try_files $uri =404;
        fastcgi_pass unix:/run/php-fpm/php-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
        include fastcgi_params;
    }
    
    location ~ /\. {
        deny all;
    }
}
EOF

# Enable
sudo ln -sf /etc/nginx/sites-available/SITENAME /etc/nginx/sites-enabled/
echo "127.0.0.1  SITENAME.l" | sudo tee -a /etc/hosts
sudo nginx -t && sudo systemctl reload nginx
```

### Quick Copy-Paste: OpenCart Site

```bash
# Replace SITENAME and PATH
sudo tee /etc/nginx/sites-available/SITENAME << 'EOF'
server {
    listen 80;
    server_name SITENAME.l;
    root /home/hruzam/www/SITENAME;
    index index.php;
    charset utf-8;
    
    error_log /var/log/nginx/SITENAME-error.log;
    access_log /var/log/nginx/SITENAME-access.log;
    
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
}
EOF

# Enable
sudo ln -sf /etc/nginx/sites-available/SITENAME /etc/nginx/sites-enabled/
echo "127.0.0.1  SITENAME.l" | sudo tee -a /etc/hosts
sudo nginx -t && sudo systemctl reload nginx
```

---

## ✅ VERIFICATION

### Full System Check

```bash
#!/bin/bash
# ~/bin/check-nginx.sh

echo "=== nginx Status ==="
systemctl status nginx | grep Active

echo ""
echo "=== PHP-FPM Status ==="
echo "PHP 7.4: $(systemctl is-active php74-fpm)"
echo "PHP 8.x: $(systemctl is-active php-fpm)"

echo ""
echo "=== Enabled Sites ==="
ls -1 /etc/nginx/sites-enabled/

echo ""
echo "=== Socket Check ==="
ls -la /run/php74-fpm/php-fpm.sock 2>/dev/null || echo "PHP 7.4 socket: NOT FOUND"
ls -la /run/php-fpm/php-fpm.sock 2>/dev/null || echo "PHP 8 socket: NOT FOUND"

echo ""
echo "=== Recent Errors ==="
sudo tail -5 /var/log/nginx/error.log

echo ""
echo "=== Test URLs ==="
for site in fantasyobchod freya psdvs; do
    echo -n "$site.l: "
    curl -I -s http://$site.l | head -1 || echo "FAILED"
done
```

**Make executable and run:**
```bash
chmod +x ~/bin/check-nginx.sh
~/bin/check-nginx.sh
```

---

**END OF NGINX MANUAL**

*Save this for reference when configuring new sites!*
*All Laravel and OpenCart patterns documented.*
