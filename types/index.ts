export interface ProcessLabel {
  text: string;
  firstWord: string;
  category: 'verb' | 'noun' | 'other';
  confidence?: number;
}

export interface AnalysisResult {
  totalLabels: number;
  verbPhrases: ProcessLabel[];
  nounPhrases: ProcessLabel[];
  others: ProcessLabel[];
  statistics: {
    verbCount: number;
    nounCount: number;
    otherCount: number;
    verbPercentage: number;
    nounPercentage: number;
    otherPercentage: number;
  };
}

export interface UploadResponse {
  success: boolean;
  data?: AnalysisResult;
  error?: string;
}
