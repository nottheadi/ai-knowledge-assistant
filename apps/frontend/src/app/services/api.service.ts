import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  baseUrl = 'https://urban-space-adventure-45qjwrjvvj5379w7-8000.app.github.dev/api';

  constructor(private http: HttpClient) {}

  uploadFile(file: File) {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post(`${this.baseUrl}/upload`, formData);
  }

  chat(query: string) {
    return this.http.post(`${this.baseUrl}/chat`, { query });
  }

  chatRag(query: string) {
    // The backend expects a JSON object: { query: ... }
    return this.http.post(
      `${this.baseUrl}/chat/RAG`,
      { query },
      {
        headers: { 'Content-Type': 'application/json' },
      },
    );
  }

  getUploadedFiles() {
    return this.http.get(`${this.baseUrl}/uploads`);
  }

  deleteFile(fileName: string) {
    return this.http.delete(`${this.baseUrl}/uploads/${encodeURIComponent(fileName)}`);
  }
}
