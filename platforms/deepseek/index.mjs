import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

export const name = 'dsh-stl-houjie';
export const inject = ['skills'];
const directory = new URL('./skills/stl-houjie/', import.meta.url);
const markdown = readFileSync(new URL('SKILL.md', directory), 'utf8');
const boundary = markdown.match(/^---\r?\n[\s\S]*?\r?\n---\r?\n/);
if (!boundary) throw new Error('The packaged skill requires YAML frontmatter');
const content = markdown.slice(boundary[0].length);

export function apply(context) {
  return context.skills.register({
    name: 'stl-houjie',
    description: '侯捷STL源码剖析：对象生存期、迭代器、容器不变量、算法契约、策略与配接器。',
    content,
    invocation: { modelInvocable: true, userInvocable: true },
    provider: name,
    source: 'bundled',
    resourceBase: { kind: 'directory', path: fileURLToPath(directory) },
  });
}
