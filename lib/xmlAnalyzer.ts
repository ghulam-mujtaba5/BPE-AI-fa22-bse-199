import { parseStringPromise } from 'xml2js';

// Word classification data structures
const COMMON_VERBS = new Set([
  'send', 'receive', 'process', 'validate', 'verify', 'create', 'delete',
  'update', 'generate', 'confirm', 'notify', 'deliver', 'suggest', 'display',
  'adjust', 'choose', 'select', 'browse', 'enter', 'download', 'retry',
  'open', 'have', 'issue', 'book'
]);

const COMMON_NOUNS = new Set([
  'customer', 'system', 'payment', 'gateway', 'user', 'account', 'ticket',
  'seat', 'match', 'process', 'notification', 'email', 'otp', 'receipt',
  'reservation', 'platform', 'database', 'server', 'end', 'sign', 'psl'
]);

export function classifyWord(word: string): 'verb' | 'noun' | 'other' {
  const lowerWord = word.toLowerCase().trim();
  
  if (COMMON_VERBS.has(lowerWord)) {
    return 'verb';
  }
  if (COMMON_NOUNS.has(lowerWord)) {
    return 'noun';
  }
  
  // Advanced heuristics
  if (lowerWord.endsWith('ing') || lowerWord.endsWith('ate') || 
      lowerWord.endsWith('ify') || lowerWord.endsWith('ize')) {
    return 'verb';
  }
  
  if (lowerWord.endsWith('tion') || lowerWord.endsWith('ment') || 
      lowerWord.endsWith('ness') || lowerWord.endsWith('ity')) {
    return 'noun';
  }
  
  return 'other';
}

export function htmlToText(html: string): string {
  if (!html) return '';
  
  // Decode HTML entities
  let text = html
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&nbsp;/g, ' ');
  
  // Remove HTML tags
  text = text.replace(/<br\s*\/?>/gi, '\n');
  text = text.replace(/<[^>]+>/g, '');
  text = text.replace(/\s+/g, ' ');
  
  return text.trim();
}

export async function extractLabelsFromXML(xmlContent: string): Promise<string[]> {
  try {
    const result = await parseStringPromise(xmlContent);
    const labels: string[] = [];
    const seen = new Set<string>();
    
    // Navigate the XML structure
    if (result.mxfile && result.mxfile.diagram) {
      for (const diagram of result.mxfile.diagram) {
        if (diagram.mxGraphModel && diagram.mxGraphModel[0].root) {
          const root = diagram.mxGraphModel[0].root[0];
          
          if (root.mxCell) {
            for (const cell of root.mxCell) {
              const attrs = cell.$;
              
              if (attrs && attrs.vertex === '1' && attrs.value) {
                const text = htmlToText(attrs.value);
                
                if (text && text.includes(' ') && !seen.has(text)) {
                  labels.push(text);
                  seen.add(text);
                }
              }
            }
          }
        }
      }
    }
    
    return labels;
  } catch (error) {
    console.error('XML parsing error:', error);
    throw new Error('Failed to parse XML file. Please ensure it is a valid draw.io diagram.');
  }
}

export function analyzeLabels(labels: string[]) {
  const verbPhrases: any[] = [];
  const nounPhrases: any[] = [];
  const others: any[] = [];
  
  for (const label of labels) {
    const words = label.split(' ');
    if (words.length === 0) continue;
    
    const firstWord = words[0];
    const category = classifyWord(firstWord);
    
    const item = {
      text: label,
      firstWord,
      category,
      confidence: category === 'other' ? 0.5 : 0.9
    };
    
    if (category === 'verb') {
      verbPhrases.push(item);
    } else if (category === 'noun') {
      nounPhrases.push(item);
    } else {
      others.push(item);
    }
  }
  
  const total = labels.length;
  
  return {
    totalLabels: total,
    verbPhrases,
    nounPhrases,
    others,
    statistics: {
      verbCount: verbPhrases.length,
      nounCount: nounPhrases.length,
      otherCount: others.length,
      verbPercentage: total > 0 ? (verbPhrases.length / total) * 100 : 0,
      nounPercentage: total > 0 ? (nounPhrases.length / total) * 100 : 0,
      otherPercentage: total > 0 ? (others.length / total) * 100 : 0,
    }
  };
}
