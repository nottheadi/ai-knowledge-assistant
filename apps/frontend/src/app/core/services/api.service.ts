import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  baseUrl = 'https://urban-space-adventure-45qjwrjvvj5379w7-8000.app.github.dev/api';
  private apiKey = 'fb3e77873421ff3214f0fc2066e2cbbe939a0362f0be72fc12c9b700447dcc9c'; // API key from backend .env

  private getHeaders() {
    return new HttpHeaders({
      'Authorization': `Bearer ${this.apiKey}`,
      'Content-Type': 'application/json',
    });
  }

  constructor(private http: HttpClient) {}

  uploadFile(file: File) {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post(`${this.baseUrl}/upload`, formData, {
      headers: new HttpHeaders({
        'Authorization': `Bearer ${this.apiKey}`,
      }),
    });
  }

  chat(query: string) {
    return this.http.post(`${this.baseUrl}/chat`, { query }, {
      headers: this.getHeaders(),
    });
  }

  chatRag(query: string) {
    return this.http.post(
      `${this.baseUrl}/chat/RAG`,
      { query },
      {
        headers: this.getHeaders(),
      },
    );
  }

  getUploadedFiles() {
    return this.http.get(`${this.baseUrl}/uploads`, {
      headers: this.getHeaders(),
      params: { _t: Date.now() }
    });
  }

  deleteFile(fileName: string) {
    return this.http.delete(`${this.baseUrl}/uploads/${encodeURIComponent(fileName)}`, {
      headers: this.getHeaders(),
    });
  }
}
