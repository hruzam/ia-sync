# Diagnosing OpenCart 404
**Status:** PHP executing, but OpenCart returns 404  
**This means:** OpenCart code is running but something's wrong internally

---

## 🔍 CRITICAL DIAGNOSTICS

### 1. Check if index.php exists and is readable
```bash
ls -la /home/hruzam/www/fantasyobchod/index.php
cat /home/hruzam/www/fantasyobchod/index.php | head -20
```

### 2. Check OpenCart error logs
```bash
# OpenCart logs errors here:
ls -la /home/hruzam/www/fantasyobchod/system/logs/
tail -50 /home/hruzam/www/fantasyobchod/system/logs/error.log 2>/dev/null || echo "No error.log yet"
```

### 3. Check if catalog directory exists
```bash
ls -la /home/hruzam/www/fantasyobchod/ | grep catalog
ls -la /home/hruzam/www/fantasyobchod/catalog/
```

### 4. Test PHP directly (bypass nginx)
```bash
cd /home/hruzam/www/fantasyobchod
php -f index.php 2>&1 | head -50
```

### 5. Check what nginx is actually serving
```bash
curl http://fantasyobchod.l 2>&1 | head -30
```

### 6. Enable PHP error display temporarily
```bash
# Check current PHP error settings
php74 -i | grep "display_errors"

# Check if index.php has error suppression
head -30 /home/hruzam/www/fantasyobchod/index.php | grep -i "display_errors\|error_reporting"
```

---

## 🔧 LIKELY CAUSES

### **Cause 1: Missing vendor/ directory (Composer dependencies)**

From the repomix, I saw OpenCart uses Tracy debugger:
```php
require __DIR__ . '/vendor/autoload.php';
```

**Check if vendor exists:**
```bash
ls -la /home/hruzam/www/fantasyobchod/ | grep vendor
```

**If missing, install dependencies:**
```bash
cd /home/hruzam/www/fantasyobchod
composer install
```

---

### **Cause 2: Database connection failing**

OpenCart might be failing to connect to database and showing 404 instead of error.

**Verify config.php database settings:**
```bash
grep "^define('DB_" /home/hruzam/www/fantasyobchod/config.php
```

**Should show:**
```php
define('DB_DRIVER', 'mysqli');
define('DB_HOSTNAME', 'localhost');
define('DB_USERNAME', 'majkee');
define('DB_PASSWORD', '<your-db-password>');   // value in ~/.config/zsh/.env/fo-db.cnf (mode 600, never committed)
define('DB_DATABASE', 'fantasyobchod');
```

**Test database connection:**
```bash
mariadb -u majkee -p fantasyobchod -e "SELECT 'Connected!' as status;"
# Enter password: (from ~/.config/zsh/.env/fo-db.cnf)
```

---

### **Cause 3: File permissions on PHP files**

**Check directory permissions:**
```bash
ls -ld /home/hruzam/www/fantasyobchod/
ls -ld /home/hruzam/www/fantasyobchod/catalog/
ls -ld /home/hruzam/www/fantasyobchod/system/
```

**All should show:**
```
drwxr-xr-x hruzam hruzam
```

**If not, fix:**
```bash
chmod 755 /home/hruzam/www/fantasyobchod/
chmod -R 755 /home/hruzam/www/fantasyobchod/catalog/
chmod -R 755 /home/hruzam/www/fantasyobchod/system/
```

---

### **Cause 4: Missing startup.php or broken includes**

**Check if critical files exist:**
```bash
ls -la /home/hruzam/www/fantasyobchod/system/startup.php
ls -la /home/hruzam/www/fantasyobchod/catalog/controller/
```

---

## 🎯 QUICK FIX ATTEMPT

**Most likely issue: vendor/ directory missing**

```bash
cd /home/hruzam/www/fantasyobchod

# Check if vendor exists
if [ ! -d "vendor" ]; then
    echo "vendor/ missing - running composer install"
    composer install
else
    echo "vendor/ exists"
fi

# Check if composer.json exists
ls -la composer.json
```

**After composer install:**
```bash
curl -I http://fantasyobchod.l
```

---

## 🔍 DEBUG MODE

**Enable verbose error display to see what's happening:**

```bash
# Edit index.php temporarily
nano /home/hruzam/www/fantasyobchod/index.php
```

**Find line 22-23 (from repomix):**
```php
//ini_set('display_errors', 'off');
ini_set('display_errors', 1);
error_reporting( E_ALL );
```

**Make sure it's ENABLED (no comment):**
```php
ini_set('display_errors', 1);
error_reporting( E_ALL );
```

**Then test again:**
```bash
curl http://fantasyobchod.l 2>&1 | head -50
```

**You should now see the actual PHP error!**

---

## 📋 RUN THESE IN ORDER

```bash
# 1. Check vendor directory
ls -la /home/hruzam/www/fantasyobchod/vendor

# 2. If missing, install
cd /home/hruzam/www/fantasyobchod && composer install

# 3. Check database connection
mariadb --defaults-extra-file=~/.config/zsh/.env/fo-db.cnf fantasyobchod -e "SELECT 'OK' as test;"

# 4. Enable errors and test
curl http://fantasyobchod.l

# 5. Check OpenCart error log
tail -20 /home/hruzam/www/fantasyobchod/system/logs/error.log
```

---

## 🎯 EXPECTED RESULTS

**If vendor/ was missing:**
- After `composer install`, OpenCart should load

**If database issue:**
- Error message about database connection
- Check config.php credentials

**If file permissions:**
- "Permission denied" in error logs
- Run chmod commands above

---

*The key is seeing the ACTUAL error. Enable display_errors and run curl to see what PHP is really saying!*
