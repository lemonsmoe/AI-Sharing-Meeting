import fs from 'node:fs/promises';
import path from 'node:path';
import {FileBlob,PresentationFile} from 'file:///C:/Users/22796/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const root=process.cwd();
const out=path.join(root,process.argv[3] || 'slides/templates/rendered');
await fs.mkdir(out,{recursive:true});
const p=await PresentationFile.importPptx(await FileBlob.load(path.join(root,process.argv[2] || 'slides/templates/sycsense_reference.pptx')));
await fs.writeFile(path.join(out,'inspection.json'),JSON.stringify(await p.inspect({kind:'slide,textbox,image,table,chart,layout',maxChars:100000}),null,2));
for(const [i,s] of p.slides.items.entries()){
 const b=await p.export({slide:s,format:'png',scale:1});
 await fs.writeFile(path.join(out,`slide_${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await b.arrayBuffer()));
 console.log(`已渲染 ${i+1}`);
}
