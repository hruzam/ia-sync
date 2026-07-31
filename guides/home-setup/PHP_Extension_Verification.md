# PHP Extension Verification Checklist
**Ensure PHP-FPM has all required extensions**  
**Machine:** @home  
**Last Updated:** March 7, 2026

---

## 🎯 QUICK FIX (Current Issue)

```bash
# XMLWriter missing
yay -S php74-xml
sudo systemctl restart php74-fpm
```

**Then verify below** ↓

---

## ✅ COMPLETE VERIFICATION

### Method 1: Browser Check (Easiest)

```bash
# Create check script
cat > ~/www/fantasyobchod/check-php.php << 'EOF'
<?php
echo "<h1>PHP Extension Check</h1>";
echo "<h2>PHP Version: " . phpversion() . "</h2>";

$required = [
    'xml' => 'XMLWriter, XMLReader, SimpleXML',
    'gd' => 'Image manipulation',
    'mysqli' => 'Database (MariaDB)',
    'curl' => 'HTTP requests',
    'mbstring' => 'Multibyte strings',
    'json' => 'JSON encode/decode',
    'soap' => 'SOAP client/server',
    'zip' => 'ZIP archives',
    'imap' => 'Email (IMAP)',
    'intl' => 'Internationalization',
];

echo "<table border='1' style='border-collapse:collapse;'>";
echo "<tr><th>Extension</th><th>Status</th><th>Purpose</th></tr>";

foreach ($required as $ext => $purpose) {
    $loaded = extension_loaded($ext);
    $status = $loaded ? '✅ Loaded' : '❌ Missing';
    $color = $loaded ? 'green' : 'red';
    echo "<tr>";
    echo "<td><strong>$ext</strong></td>";
    echo "<td style='color:$color'>$status</td>";
    echo "<td>$purpose</td>";
    echo "</tr>";
}

echo "</table>";

// Show ALL loaded extensions
echo "<h2>All Loaded Extensions</h2>";
echo "<pre>";
print_r(get_loaded_extensions());
echo "</pre>";
?>
EOF

# Open in browser
firefox http://fantasyobchod.l/check-php.php
```

**Look for red ❌ marks and install missing extensions**

---

### Method 2: Command Line Check

```bash
# Check specific extension
php -m | grep -i xml
php -m | grep -i gd
php -m | grep -i mysqli

# OR create test script
cat > check-cli.php << 'EOF'
<?php
$required = ['xml', 'gd', 'mysqli', 'curl', 'mbstring', 'json', 'soap', 'zip', 'imap'];
foreach ($required as $ext) {
    $status = extension_loaded($ext) ? '✅' : '❌';
    echo "$status $ext\n";
}
EOF

php check-cli.php
```

---

## 📦 INSTALLATION REFERENCE

### Core Extensions (Required)

```bash
# XML (XMLWriter, XMLReader, SimpleXML)
yay -S php74-xml
# For: google_base.php feeds, XML parsing

# GD (Image manipulation)
yay -S php74-gd
# For: Image resizing, watermarks, thumbnails

# MySQL/MariaDB
yay -S php74-mysql
# For: Database connections

# cURL
yay -S php74-curl
# For: HTTP requests, API calls

# mbstring
yay -S php74-mbstring
# For: Multibyte string handling (UTF-8)

# JSON
yay -S php74-json
# For: JSON encode/decode

# After installing ANY extension:
sudo systemctl restart php74-fpm
```

### Optional But Recommended

```bash
# SOAP
yay -S php74-soap
# For: Payment gateways (GoPay, etc.)

# ZIP
yay -S php74-zip
# For: Backup exports, file compression

# IMAP
yay -S php74-imap
# For: Email handling

# Intl
yay -S php74-intl
# For: Internationalization, date formatting
```

---

## 🔍 FROM COMPOSER.JSON

**Your composer.json requires these:**

```json
{
  "require": {
    "ulozenka/api-v3": "...",        // → curl
    "tracy/tracy": "...",             // → mbstring
    "guzzlehttp/guzzle": "...",       // → curl
    "php-imap/php-imap": "...",       // → imap
    "phpoffice/phpexcel": "...",      // → xml, zip, gd
    "markette/gopay-inline": "...",   // → soap, curl
    "mpdf/mpdf": "...",               // → gd, mbstring
  }
}
```

**Minimum required extensions from dependencies:**
- ✅ xml
- ✅ gd
- ✅ curl
- ✅ mbstring
- ✅ json
- ✅ mysqli
- ✅ soap (for payment gateways)
- ✅ imap (for php-imap package)
- ✅ zip (for PHPExcel)

---

## 🚨 TROUBLESHOOTING

### Extension Installed But Still Error

**Problem:** Extension installed but not loaded

**Check:**
```bash
# Is extension file present?
ls /usr/lib/php74/modules/ | grep xml
# Should show: xml.so

# Is it enabled in php.ini?
grep -i "extension=xml" /etc/php74/php.ini

# Did you restart FPM?
sudo systemctl restart php74-fpm
sudo systemctl status php74-fpm
```

**Fix:**
```bash
# If not in php.ini, add it
echo "extension=xml" | sudo tee -a /etc/php74/php.ini

# Restart
sudo systemctl restart php74-fpm
```

### Wrong PHP Version Showing

**Problem:** `php -v` shows PHP 8.5.3

**This is NORMAL!**

```bash
# System PHP (CLI)
php -v
# Shows: PHP 8.5.3 ← System default, NOT used by website

# PHP-FPM (Website)
systemctl status php74-fpm
# Shows: Active (running) ← This is what runs the website

# To check FPM version, use browser:
echo "<?php phpinfo(); ?>" > ~/www/fantasyobchod/phpinfo.php
firefox http://fantasyobchod.l/phpinfo.php
# Look for: PHP Version 7.4.33
```

---

## 📋 INSTALLATION CHECKLIST

**Copy-paste this into terminal:**

```bash
#!/bin/bash
# Install all required PHP 7.4 extensions

echo "Installing PHP 7.4 extensions..."

# Core extensions
yay -S --needed php74-xml php74-gd php74-mysql php74-curl php74-mbstring php74-json

# Optional but recommended
yay -S --needed php74-soap php74-zip php74-imap php74-intl

# Restart PHP-FPM
sudo systemctl restart php74-fpm

echo "Done! Verify at: http://fantasyobchod.l/check-php.php"
```

**After running, check:**
```bash
firefox http://fantasyobchod.l/check-php.php
```

---

## 🎯 PROJECT-SPECIFIC NEEDS

### FantasyObchod (OpenCart)

**Based on your composer.json:**

```bash
# Minimum required
yay -S php74-xml       # ← XMLWriter for google_base.php
yay -S php74-gd        # ← Image manipulation
yay -S php74-mysql     # ← Database
yay -S php74-curl      # ← API calls (Ulozenka, GoPay)
yay -S php74-mbstring  # ← UTF-8 handling
yay -S php74-json      # ← JSON API responses
yay -S php74-soap      # ← Payment gateways
yay -S php74-imap      # ← Email processing
yay -S php74-zip       # ← PHPExcel exports

# Restart
sudo systemctl restart php74-fpm
```

### Freya/PSDVS (Laravel)

**When you configure these, you'll need:**

```bash
# Laravel typically requires:
yay -S php-xml       # (PHP 8+, different package!)
yay -S php-mbstring
yay -S php-curl
yay -S php-gd
yay -S php-zip
yay -S php-intl

# Restart
sudo systemctl restart php-fpm  # Note: php-fpm, not php74-fpm
```

---

## 🔄 MAINTENANCE

### After System Update

```bash
# Manjaro updates might reset PHP configs

# Re-check extensions
firefox http://fantasyobchod.l/check-php.php

# If any missing, reinstall
yay -S php74-[extension]
sudo systemctl restart php74-fpm
```

### After New Package Added

```bash
# When you run: composer74 require vendor/new-package

# Check if it needs new extension
cat vendor/new-package/composer.json | grep "ext-"

# If shows: "ext-imagick": "*"
# Then install: yay -S php74-imagick
```

---

## ✅ VERIFICATION SCRIPT

**Save this for future use:**

```bash
# ~/bin/check-php-extensions.sh

#!/bin/bash

echo "=== PHP-FPM Extension Check ==="
echo ""

# Check service
if systemctl is-active --quiet php74-fpm; then
    echo "✅ PHP-FPM is running"
else
    echo "❌ PHP-FPM is NOT running"
    echo "   Fix: sudo systemctl start php74-fpm"
    exit 1
fi

# Check extensions via web
if curl -s http://fantasyobchod.l/check-php.php | grep -q "❌"; then
    echo "❌ Some extensions missing"
    echo "   View: firefox http://fantasyobchod.l/check-php.php"
else
    echo "✅ All required extensions loaded"
fi

echo ""
echo "Full report: http://fantasyobchod.l/check-php.php"
```

**Make executable:**
```bash
chmod +x ~/bin/check-php-extensions.sh
```

**Use:**
```bash
~/bin/check-php-extensions.sh
```

---

## 📞 QUICK HELP

### Error Pattern Recognition

| Error Message | Missing Extension | Fix |
|---------------|-------------------|-----|
| Class 'XMLWriter' not found | xml | `yay -S php74-xml` |
| Call to undefined function imagecreate | gd | `yay -S php74-gd` |
| Call to undefined function mysqli_connect | mysql | `yay -S php74-mysql` |
| Call to undefined function curl_init | curl | `yay -S php74-curl` |
| Call to undefined function mb_strlen | mbstring | `yay -S php74-mbstring` |
| Call to undefined function json_encode | json | `yay -S php74-json` |
| Class 'SoapClient' not found | soap | `yay -S php74-soap` |
| Class 'ZipArchive' not found | zip | `yay -S php74-zip` |

**Always restart after install:**
```bash
sudo systemctl restart php74-fpm
```

---

**END OF CHECKLIST**

*Keep check-php.php in your project for quick verification!*
*Delete it after verification or add to .gitignore*
