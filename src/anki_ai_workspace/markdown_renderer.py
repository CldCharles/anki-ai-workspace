from __future__ import annotations

# This script deliberately escapes input before producing a small, known set of
# HTML elements. It is bundled with the add-on so reviewer rendering has no
# network dependency.
MARKDOWN_RENDERER_SCRIPT = r"""
window.AnkiAIWorkspaceMarkdown=(()=>{
  const escapeHtml=value=>String(value).replace(/[&<>"']/g,character=>({
    '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
  })[character]);
  const safeHref=value=>{
    const href=String(value).replace(/&amp;/g,'&').trim();
    return /^(https?:\/\/|mailto:)[^\s]+$/i.test(href)?href:null;
  };
  const inline=value=>{
    const tokens=[];
    const token=html=>`\u0000${tokens.push(html)-1}\u0000`;
    let text=escapeHtml(value);
    text=text.replace(/`([^`\n]+)`/g,(_match,content)=>token(`<code>${content}</code>`));
    text=text.replace(/\[([^\]]+)\]\(([^\s)]+)\)/g,(_match,label,href)=>{
      const safe=safeHref(href);
      return safe?token(`<a href="${escapeHtml(safe)}" target="_blank" rel="noopener noreferrer">${inline(label)}</a>`):_match;
    });
    text=text.replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>');
    text=text.replace(/__(.+?)__/g,'<strong>$1</strong>');
    text=text.replace(/(^|[^*])\*([^*\n]+)\*(?!\*)/g,'$1<em>$2</em>');
    text=text.replace(/(^|[^_])_([^_\n]+)_(?!_)/g,'$1<em>$2</em>');
    return text.replace(/\u0000(\d+)\u0000/g,(_match,index)=>tokens[Number(index)]);
  };
  const tableCells=line=>line.trim().replace(/^\||\|$/g,'').split('|').map(cell=>cell.trim());
  const isTableDivider=line=>/^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$/.test(line);
  const isBlockStart=line=>/^(?:\s*```|\s{0,3}#{1,6}\s+|\s*>|\s*[-+*]\s+|\s*\d+\.\s+)/.test(line);
  const blocks=source=>{
    const lines=String(source).replace(/\r\n?/g,'\n').split('\n');
    const result=[];
    let index=0;
    while(index<lines.length){
      const line=lines[index];
      if(!line.trim()){index+=1;continue;}
      if(/^\s*```/.test(line)){
        const content=[];index+=1;
        while(index<lines.length&&!/^\s*```/.test(lines[index])){content.push(lines[index]);index+=1;}
        if(index<lines.length)index+=1;
        result.push(`<pre><code>${escapeHtml(content.join('\n'))}</code></pre>`);continue;
      }
      const heading=line.match(/^\s{0,3}(#{1,6})\s+(.+)$/);
      if(heading){const level=heading[1].length;result.push(`<h${level}>${inline(heading[2])}</h${level}>`);index+=1;continue;}
      if(index+1<lines.length&&line.includes('|')&&isTableDivider(lines[index+1])){
        const header=tableCells(line), rows=[];index+=2;
        while(index<lines.length&&lines[index].includes('|')&&lines[index].trim()){
          rows.push(tableCells(lines[index]));index+=1;
        }
        result.push(`<table><thead><tr>${header.map(cell=>`<th>${inline(cell)}</th>`).join('')}</tr></thead><tbody>${rows.map(row=>`<tr>${header.map((_cell,column)=>`<td>${inline(row[column]||'')}</td>`).join('')}</tr>`).join('')}</tbody></table>`);continue;
      }
      if(/^\s*>/.test(line)){
        const quote=[];
        while(index<lines.length&&/^\s*>/.test(lines[index])){quote.push(lines[index].replace(/^\s*>\s?/,''));index+=1;}
        result.push(`<blockquote>${blocks(quote.join('\n'))}</blockquote>`);continue;
      }
      const unordered=line.match(/^\s*[-+*]\s+(.+)$/),ordered=line.match(/^\s*\d+\.\s+(.+)$/);
      if(unordered||ordered){
        const orderedList=Boolean(ordered),items=[];
        const expression=orderedList?/^\s*\d+\.\s+(.+)$/:/^\s*[-+*]\s+(.+)$/;
        while(index<lines.length){const item=lines[index].match(expression);if(!item)break;items.push(`<li>${inline(item[1])}</li>`);index+=1;}
        result.push(`<${orderedList?'ol':'ul'}>${items.join('')}</${orderedList?'ol':'ul'}>`);continue;
      }
      const paragraph=[line];index+=1;
      while(index<lines.length&&lines[index].trim()&&!isBlockStart(lines[index])&&!(lines[index].includes('|')&&index+1<lines.length&&isTableDivider(lines[index+1]))){paragraph.push(lines[index]);index+=1;}
      result.push(`<p>${paragraph.map(inline).join('<br>')}</p>`);
    }
    return result.join('');
  };
  return {render:blocks};
})();
"""
