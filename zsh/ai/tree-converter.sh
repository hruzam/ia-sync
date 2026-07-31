#!/bin/bash
# folder-tree-formater.sh

CONFIG_FILE=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -c|--c|--config)
      CONFIG_FILE="$2"
      shift 2
      ;;
    --config=*)
      CONFIG_FILE="${1#*=}"
      shift 1
      ;;
    *)
      # Ignore unknown arguments
      shift 1
      ;;
  esac
done

# Create a temporary Node.js script to handle the heavy lifting natively
TMP_SCRIPT=$(mktemp /tmp/tree-formater.XXXXXX.js)

cat << 'EOF' > "$TMP_SCRIPT"
const fs = require('fs');
const path = require('path');

const configArg = process.argv[2];

// 1. Establish Approved Defaults
let config = {
    output: { style: 'json' }, // No filePath = console stdout
    tree: { level: Infinity, showHidden: false },
    include: [], // Empty include array means grab everything
    ignore: {
        useGitignore: true,
        useDefaultPatterns: true,
        customPatterns: ['.git/**', 'node_modules/**']
    }
};

// 2. Load & Merge Custom Config (Supports .json and .js)
if (configArg && configArg !== "undefined" && configArg !== "") {
    try {
        const absolutePath = path.resolve(process.cwd(), configArg);
        const userConfig = require(absolutePath);

        // Safely merge user config over defaults
        config = {
            output: { ...config.output, ...(userConfig.output || {}) },
            tree: { ...config.tree, ...(userConfig.tree || {}) },
            include: userConfig.include || config.include,
            ignore: { ...config.ignore, ...(userConfig.ignore || {}) }
        };
    } catch (err) {
        console.error(`[Rivet] Error: Could not load config file at '${configArg}'`);
        console.error(err.message);
        process.exit(1);
    }
}

// Extract tree parameters
const maxLevel = config.tree?.level ? parseInt(config.tree.level, 10) : Infinity;
const showHidden = config.tree?.showHidden === true;

// Convert config globs into regex
function makeRegex(globPattern) {
    if (globPattern.startsWith('/')) globPattern = globPattern.slice(1);
    let str = globPattern
        .replace(/\./g, '\\.')
        .replace(/\*\*/g, '____GLOB_STAR____')
        .replace(/\*/g, '[^/]*')
        .replace(/____GLOB_STAR____/g, '.*');

    if (!globPattern.endsWith('*')) {
        str = str + '($|/.*)';
    } else {
        str = str + '$';
    }
    return new RegExp(`^${str}`);
}

const ignoreRegexes = [];
const includeRegexes = [];

if (config.ignore?.customPatterns) {
    config.ignore.customPatterns.forEach(p => ignoreRegexes.push(makeRegex(p)));
}
if (config.ignore?.useGitignore && fs.existsSync('.gitignore')) {
    fs.readFileSync('.gitignore', 'utf8').split('\n').forEach(line => {
        line = line.trim();
        if (line && !line.startsWith('#')) ignoreRegexes.push(makeRegex(line));
    });
}

if (config.include) {
    config.include.forEach(p => includeRegexes.push(makeRegex(p)));
}

// Fast Directory Crawler with Depth & Hidden checks
function getFiles(dir, fileList = [], baseDir = '', currentDepth = 1) {
    let entries;
    try {
        entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch (e) {
        return fileList;
    }

    for (const entry of entries) {
        if (!showHidden && entry.name.startsWith('.')) continue;

        const relativePath = path.join(baseDir, entry.name).replace(/\\/g, '/');

        let ignored = false;
        for (const ig of ignoreRegexes) {
            if (ig.test(relativePath)) { ignored = true; break; }
        }
        if (ignored) continue;

        if (entry.isDirectory()) {
            if (currentDepth < maxLevel) {
                getFiles(path.join(dir, entry.name), fileList, relativePath, currentDepth + 1);
            }
        } else {
            let included = includeRegexes.length === 0;
            for (const inc of includeRegexes) {
                if (inc.test(relativePath)) { included = true; break; }
            }
            if (included) {
                fileList.push(relativePath);
            }
        }
    }
    return fileList;
}

const files = getFiles('.');

// Build the JSON Tree structure
function buildTree(paths) {
    const root = {};
    for (const p of paths) {
        const parts = p.split('/');
        let current = root;
        for (let i = 0; i < parts.length; i++) {
            const part = parts[i];
            const isFile = i === parts.length - 1;
            if (isFile) {
                if (!current._files) current._files = [];
                current._files.push(part);
            } else {
                if (!current[part]) current[part] = {};
                current = current[part];
            }
        }
    }

    function cleanup(node) {
        const result = {};
        const keys = Object.keys(node).sort();

        for (const k of keys) {
            if (k !== '_files') result[k] = cleanup(node[k]);
        }
        if (node._files) {
             node._files.sort();
             if (Object.keys(result).length === 0) return node._files;
             result["_files"] = node._files;
        }
        return result;
    }
    return cleanup(root);
}

const tree = buildTree(files);

// Dependency-free YAML serializer
function toYAML(obj, indent = 0) {
    let yaml = '';
    const spaces = '  '.repeat(indent);
    if (Array.isArray(obj)) {
        for (const item of obj) yaml += `${spaces}- ${item}\n`;
    } else if (typeof obj === 'object' && obj !== null) {
        for (const [key, val] of Object.entries(obj)) {
            if (Array.isArray(val) && val.length > 0) {
                yaml += `${spaces}${key}:\n` + toYAML(val, indent + 1);
            } else if (typeof val === 'object' && val !== null && Object.keys(val).length > 0) {
                yaml += `${spaces}${key}:\n` + toYAML(val, indent + 1);
            } else if (Array.isArray(val) && val.length === 0) {
                yaml += `${spaces}${key}: []\n`;
            } else if (typeof val === 'object' && val !== null && Object.keys(val).length === 0) {
                 yaml += `${spaces}${key}: {}\n`;
            } else {
                yaml += `${spaces}${key}: ${val}\n`;
            }
        }
    }
    return yaml;
}

const outStyle = (config.output?.style || 'json').toLowerCase();
let outputStr = '';

if (outStyle === 'yaml' || outStyle === 'yml') {
    outputStr = toYAML(tree);
} else {
    outputStr = JSON.stringify(tree, null, 2);
}

const rawFilePath = config.output?.filePath;
const ext = (outStyle === 'yaml' || outStyle === 'yml') ? 'yaml' : 'json';
const outFile = (rawFilePath && rawFilePath !== '.')
    ? (rawFilePath.endsWith('.' + ext) ? rawFilePath : `${rawFilePath}.${ext}`)
    : null;

if (outFile) {
    const dir = path.dirname(outFile);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

    fs.writeFileSync(outFile, outputStr);
    console.log(`[Rivet] Output successfully formatted and saved to -> ${outFile}`);
} else {
    // Print to console if no filePath is specified
    console.log(outputStr);
}
EOF

# Execute the script and pass the config file argument
node "$TMP_SCRIPT" "$CONFIG_FILE"
rm "$TMP_SCRIPT"
