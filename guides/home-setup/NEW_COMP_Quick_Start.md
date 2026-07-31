# AI Collaborator Quick Start Guide
**Essential context for @Cursor, @Vega, and other AI agents**  
**Machine:** @home (Manjaro KDE Plasma)  
**Last Updated:** March 7, 2026

---

## 🎯 CRITICAL CONCEPT: TWO SEPARATE PHP ENVIRONMENTS

**This is the #1 source of confusion!**

### Environment 1: Docker (Composer Only)

```
Purpose: composer install/update/dump-autoload
PHP Version: 7.4.33 (inside container)
Extensions: zip, imap, soap, mbstring, xml, gd
Used by: composer74 command
Does NOT run: website code
Location: Docker container (ephemeral)
```

**When you use:**
```bash
composer74 install
composer74 update
composer74 require vendor/package
```

### Environment 2: PHP-FPM (Website Runtime)

```
Purpose: Running actual website via nginx
PHP Version: 7.4.33 (native Manjaro package)
Extensions: MUST be installed separately!
Used by: nginx → PHP-FPM → runs google_base.php, etc.
Runs: ALL website code
Location: /usr/bin/php-fpm74
```

**When user accesses:**
```
http://fantasyobchod.l
http://fantasyobchod.l/admin
```

---

## 🔍 DIAGNOSTIC: Which PHP is Running?

### For Composer (Docker)

```bash
# Check PHP version in Docker
docker run --rm --entrypoint php php74-composer -v
# Output: PHP 7.4.33 (cli)

# Check extensions in Docker
docker run --rm --entrypoint php php74-composer -m
# Lists all extensions available to composer
```

### For Website (PHP-FPM)

```bash
# Check PHP-FPM version
systemctl status php74-fpm
# Shows: Active (running)

# Check CLI version (NOT what FPM uses!)
php -v
# Shows: PHP 8.5.3 ← This is system default, IGNORE!

# Check actual FPM extensions
php74 -m  # IF php74 binary exists (it doesn't on @home)
# OR: Create test file
```

**Create test file to check FPM:**

```bash
echo "<?php phpinfo(); ?>" > ~/www/fantasyobchod/phpinfo.php
firefox http://fantasyobchod.l/phpinfo.php
# Search for "Loaded extensions"
```

---

## 📦 EXTENSION INSTALLATION MATRIX

### Docker Container (Composer)

**Already installed in Dockerfile:**
```
✅ zip
✅ imap  
✅ soap
✅ mbstring
✅ xml (includes XMLWriter, XMLReader)
✅ gd
```

**To add new extension to Docker:**

```bash
# 1. Edit Dockerfile
nano ~/.docker/php74-composer/Dockerfile

# 2. Add extension
RUN docker-php-ext-install new-extension

# 3. Rebuild
cd ~/.docker/php74-composer
docker build -t php74-composer .
```

### PHP-FPM (Website)

**Installation via AUR packages:**

| Extension | Package | Install Command |
|-----------|---------|-----------------|
| xml | php74-xml | `yay -S php74-xml` |
| gd | php74-gd | `yay -S php74-gd` |
| curl | php74-curl | `yay -S php74-curl` |
| mbstring | php74-mbstring | `yay -S php74-mbstring` |
| mysqli | php74-mysql | `yay -S php74-mysql` |
| soap | php74-soap | `yay -S php74-soap` |
| imap | php74-imap | `yay -S php74-imap` |
| zip | php74-zip | `yay -S php74-zip` |
| intl | php74-intl | `yay -S php74-intl` |
| json | php74-json | `yay -S php74-json` |

**After installing:**
```bash
sudo systemctl restart php74-fpm
```

---

## 🚨 COMMON ERROR PATTERNS

### Error: "Class 'XMLWriter' not found"

**Diagnosis:**
```
Error in: Website code (google_base.php)
Missing in: PHP-FPM environment
Solution: Install php74-xml for FPM
```

**Fix:**
```bash
yay -S php74-xml
sudo systemctl restart php74-fpm
```

### Error: "Call to undefined function imagecreatetruecolor()"

**Diagnosis:**
```
Error in: Image manipulation code
Missing in: PHP-FPM environment
Solution: Install php74-gd for FPM
```

**Fix:**
```bash
yay -S php74-gd
sudo systemctl restart php74-fpm
```

### Error: Composer package requires extension X

**Diagnosis:**
```
Error during: composer74 install
Missing in: Docker container
Solution: Add to Dockerfile
```

**Fix:**
```bash
nano ~/.docker/php74-composer/Dockerfile
# Add extension
docker build -t php74-composer ~/.docker/php74-composer/
```

---

## 🔧 PROJECT STRUCTURE

### File Locations

```
~/www/fantasyobchod/              ← Project code
├── google_base.php               ← Example: XML feed generator
├── vendor/                       ← Composer packages (from Docker)
├── composer.json                 ← Dependencies
├── system/
│   ├── library/                  ← Custom classes
│   └── storage/                  ← Writable (http:http)
└── admin/
    └── module/
        ├── core/                 ← Abstract classes
        └── library/              ← Concrete modules

~/.docker/php74-composer/         ← Docker setup
├── Dockerfile                    ← PHP 7.4 + extensions
└── (ephemeral containers)

/etc/php74/                       ← PHP-FPM config
├── php.ini                       ← PHP settings
└── php-fpm.d/www.conf            ← FPM pool config

/etc/nginx/                       ← Web server
└── sites-available/fantasyobchod ← Site config
```

---

## 🔄 WORKFLOW: Adding New Functionality

### Step 1: Check Dependencies

```bash
# Does the code use any PHP extensions?
# Example: XMLWriter, GD, SOAP, etc.
grep -r "new XMLWriter" ~/www/fantasyobchod/
grep -r "imagecreate" ~/www/fantasyobchod/
```

### Step 2: Verify in BOTH Environments

**Composer (Docker):**
```bash
docker run --rm --entrypoint php php74-composer -m | grep -i xml
```

**PHP-FPM (Website):**
```bash
# Create test
echo "<?php echo extension_loaded('xml') ? 'YES' : 'NO'; ?>" > ~/www/fantasyobchod/test.php
curl http://fantasyobchod.l/test.php
```

### Step 3: Install Where Missing

**Missing in Docker?** → Edit Dockerfile + rebuild
**Missing in FPM?** → `yay -S php74-extension` + restart

---

## 📋 VERIFICATION CHECKLIST

### Before Running Code

```bash
# 1. Check PHP-FPM running
systemctl status php74-fpm
# Should be: active (running)

# 2. Check required extensions
# Create: ~/www/fantasyobchod/check-extensions.php

<?php
$required = ['xml', 'gd', 'mysqli', 'curl', 'mbstring', 'json', 'soap'];
foreach ($required as $ext) {
    echo $ext . ': ' . (extension_loaded($ext) ? '✅' : '❌') . "\n";
}
?>

# 3. Access via browser
firefox http://fantasyobchod.l/check-extensions.php

# 4. If any ❌, install
yay -S php74-[extension]
sudo systemctl restart php74-fpm
```

---

## 🎯 QUICK FIXES

### Website Error: Extension Missing

```bash
# Pattern: Class 'X' not found OR Call to undefined function X()
# Example: XMLWriter, imagecreate, curl_init, etc.

# 1. Identify extension needed
# XMLWriter → xml
# imagecreate → gd
# curl_init → curl
# mysqli_connect → mysql

# 2. Install for PHP-FPM
yay -S php74-[extension]

# 3. Restart
sudo systemctl restart php74-fpm

# 4. Verify
curl http://fantasyobchod.l/[your-page]
```

### Composer Error: Extension Missing

```bash
# Pattern: ext-X is missing from your system

# 1. Edit Dockerfile
nano ~/.docker/php74-composer/Dockerfile

# 2. Add extension
RUN docker-php-ext-install [extension]

# 3. Rebuild
cd ~/.docker/php74-composer
docker build -t php74-composer .

# 4. Retry
cd ~/www/fantasyobchod
composer74 install
```

---

## 📚 DOCUMENTATION REFERENCES

**For detailed setup:**
- OpenCart_Home_Setup_Complete_Guide.md
- FantasyObchod_Home_Quick_Reference.md
- Docker_PHP74_Complete_Setup.md

**For architecture:**
- FantasyObchod_Technical_Standards.md (Google Drive)
- module_architecture_deep_dive.md (repo docs/)

**For daily commands:**
- FantasyObchod_Home_Quick_Reference.md

---

## 🎭 FOR @CURSOR SPECIFICALLY

### What You Can Do

```
✅ Read code
✅ Suggest fixes
✅ Generate code
✅ Explain errors
✅ Debug logic
```

### What You CANNOT Do (Need @majkee)

```
❌ Install PHP extensions (requires: yay -S)
❌ Restart services (requires: sudo systemctl)
❌ Edit system configs (requires: sudo nano)
❌ Run composer (requires: composer74 command in ZSH)
```

### Your Workflow

**When analyzing error:**

1. **Identify WHERE error occurs**
   - Composer install? → Docker environment
   - Website runtime? → PHP-FPM environment

2. **Check WHAT is missing**
   - Class 'X' not found → Usually extension
   - Undefined function → Usually extension
   - Composer error → Package or Docker extension

3. **Tell @majkee WHICH environment needs fix**
   - "Install php74-xml for PHP-FPM"
   - "Add extension to Dockerfile"

**Example Good Response:**

```
Error: Class 'XMLWriter' not found in google_base.php

Analysis:
- Error occurs at: Website runtime (PHP-FPM)
- Missing: xml extension
- NOT a composer issue (Docker is fine)

Solution for @majkee:
1. Run: yay -S php74-xml
2. Run: sudo systemctl restart php74-fpm
3. Test: curl http://fantasyobchod.l/google_base.php

This is a PHP-FPM extension issue, not a code issue.
```

---

## 🔐 PERMISSIONS REFERENCE

### File Ownership

```
Project files: hruzam:hruzam (your user)
Writable dirs: http:http (web server)
  - system/storage/
  - system/cache/
  - tracy/
  - admin/tracy/
  - ~/www/sessions/
```

### Common Permission Fixes

```bash
# After git pull (files owned by you)
cd ~/www/fantasyobchod

# Make storage writable by web server
sudo chown -R http:http system/storage/ system/cache/
sudo chown -R http:http tracy/ admin/tracy/

# Keep code owned by you
sudo chown -R hruzam:hruzam *.php system/library/ admin/
```

---

## 🚀 NEXT SESSION PREPARATION

### For Clean Context with @Houston

**Upload these files:**
```
1. composer.json (dependencies)
2. Relevant PHP file (e.g., google_base.php)
3. Error message (if any)
4. This Quick Start Guide (for reference)
```

**Start conversation with:**
```
[CONTEXT: @home]
[PROJECT: FantasyObchod]
Problem: [describe issue]
Error: [paste error]
```

### For @Cursor Code Review

**Provide:**
```
1. File being edited (e.g., google_base.php)
2. Error message
3. Expected behavior
4. This Quick Start (so @Cursor understands environment)
```

**Ask:**
```
"@Cursor, review this code considering:
- Runs on PHP 7.4 FPM
- Available extensions: [list from phpinfo]
- OpenCart 2.x architecture
"
```

---

## ✅ IMMEDIATE FIX FOR CURRENT ERROR

```bash
# XMLWriter missing in PHP-FPM

# Install
yay -S php74-xml

# Restart
sudo systemctl restart php74-fpm

# Verify
echo "<?php var_dump(class_exists('XMLWriter')); ?>" > ~/www/fantasyobchod/test.php
curl http://fantasyobchod.l/test.php
# Should output: bool(true)

# Remove test
rm ~/www/fantasyobchod/test.php

# Test actual script
curl http://fantasyobchod.l/[path-to-google_base.php]
```

---

**END OF QUICK START**

*This document explains the critical Docker vs FPM distinction.*
*Share with @Cursor to avoid confusion about two PHP environments!*
