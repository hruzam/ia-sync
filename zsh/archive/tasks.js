// Task Registry Tree
// Loaded by zsh task commands, normalizes paths across projects
// Usage: node ~/.config/zsh/registries/tasks.js [list|add|done|help] [args]

const fs = require('fs');
const path = require('path');
const os = require('os');

// Project branches - add new projects here
const BRANCHES = {
    larva: path.join(os.homedir(), 'www/larva_dev/dev/.config/tasks.jsonl'),
    // fo: path.join(os.homedir(), 'www/fantasyobchod/dev/.config/tasks.jsonl'),
};

const DEFAULT_BRANCH = 'larva';

// Helpers
function readTasks(branch) {
    const file = BRANCHES[branch];
    if (!file || !fs.existsSync(file)) return [];
    return fs.readFileSync(file, 'utf8')
        .trim()
        .split('\n')
        .filter(line => line)
        .map(line => JSON.parse(line));
}

function writeTasks(branch, tasks) {
    const file = BRANCHES[branch];
    if (!file) return false;
    fs.writeFileSync(file, tasks.map(t => JSON.stringify(t)).join('\n') + '\n');
    return true;
}

function appendTask(branch, task) {
    const file = BRANCHES[branch];
    if (!file) return false;
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.appendFileSync(file, JSON.stringify(task) + '\n');
    return true;
}

function genId() {
    return 'task-' + Math.random().toString(36).substr(2, 6);
}

function formatTask(t, index) {
    const status = t.status === 'open' ? '[ ]' : t.status === 'waiting' ? '[~]' : '[x]';
    const who = t.who ? `@${t.who}` : '';
    return `${status} ${t.title} ${who}`.trim();
}

// Commands
const cmd = process.argv[2] || 'list';
const args = process.argv.slice(3);

switch (cmd) {
    case 'list':
    case 'ls': {
        const branch = args[0] || 'all';
        const branches = branch === 'all' ? Object.keys(BRANCHES) : [branch];

        branches.forEach(b => {
            if (!BRANCHES[b]) return;
            const tasks = readTasks(b);
            const open = tasks.filter(t => t.status !== 'done');
            if (open.length === 0) return;

            console.log(`\n=== ${b.toUpperCase()} ===`);
            open.forEach((t, i) => console.log(formatTask(t, i)));
        });
        console.log('');
        break;
    }

    case 'add': {
        const title = args[0];
        const branch = args[1] || DEFAULT_BRANCH;
        if (!title) {
            console.log('Usage: tasks add "title" [branch]');
            process.exit(1);
        }
        const task = {
            id: genId(),
            ts: new Date().toISOString(),
            status: 'open',
            title: title,
            context: null,
            ref: null,
            who: process.env.USER || 'unknown'
        };
        appendTask(branch, task);
        console.log(`Added to ${branch}: ${title}`);
        break;
    }

    case 'done': {
        const query = args[0];
        const branch = args[1] || DEFAULT_BRANCH;
        if (!query) {
            console.log('Usage: tasks done "search" [branch]');
            process.exit(1);
        }
        const tasks = readTasks(branch);
        const idx = tasks.findIndex(t => t.title.toLowerCase().includes(query.toLowerCase()) && t.status !== 'done');
        if (idx === -1) {
            console.log('Task not found');
            process.exit(1);
        }
        tasks[idx].status = 'done';
        tasks[idx].done_at = new Date().toISOString();
        writeTasks(branch, tasks);
        console.log(`Done: ${tasks[idx].title}`);
        break;
    }

    case 'help':
    default:
        console.log(`
Task Registry - Multi-project task tracking

Usage:
  tasks list [branch|all]     List open tasks
  tasks add "title" [branch]  Add new task
  tasks done "search" [branch] Mark task done

Branches: ${Object.keys(BRANCHES).join(', ')}
Default: ${DEFAULT_BRANCH}

Aliases (add to zsh):
  alias tasks='node ~/.config/zsh/registries/tasks.js'
  alias '! tasks'='tasks list'
`);
}
