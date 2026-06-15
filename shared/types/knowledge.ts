export interface Document {
  id: string;
  filename: string;
  file_type: "pdf" | "docx" | "md" | "txt";
  size_bytes: number;
  chunk_count: number;
  uploaded_at: string;
}

export interface KnowledgeChunk {
  id: string;
  document_id: string;
  content: string;
  embedding?: number[];
  metadata: Record<string, unknown>;
}

export interface SearchQuery {
  query: string;
  top_k?: number;
  filters?: Record<string, string>;
}

export interface SearchResult {
  chunk: KnowledgeChunk;
  score: number;
  document: Document;
}
