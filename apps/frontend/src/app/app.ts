import { Component, ElementRef, signal, ViewChild, OnInit, ChangeDetectorRef } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { marked } from 'marked';
import { RouterOutlet } from '@angular/router';
import { ApiService } from './services/api.service';
import { ToastService } from './services/toast.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

import { MessageListComponent } from './components/message-list.component';
import { ChatInputComponent } from './components/chat-input.component';
import { ToastContainerComponent } from './components/toast-container.component';

export interface UploadedFile {
  name: string;
  size: number;
  uploadedAt: Date;
}

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, FormsModule, CommonModule, MessageListComponent, ChatInputComponent, ToastContainerComponent],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App implements OnInit {
  protected readonly title = signal('frontend');

  selectedFile!: File;
  uploadedFiles: UploadedFile[] = [];
  query = '';
  messages: any[] = [];
  isLoading = false;
  loadingPhase: 'none' | 'thinking' | 'refining' | 'formatting' = 'none';
  isLoadingFiles = false;

  @ViewChild('chatWindow') chatWindow!: ElementRef;

  constructor(
    private api: ApiService,
    private cdr: ChangeDetectorRef,
    private sanitizer: DomSanitizer,
    private toast: ToastService,
  ) {}

  ngOnInit(): void {
    this.fetchUploadedFiles();
  }

  fetchUploadedFiles() {
    this.isLoadingFiles = true;
    this.api.getUploadedFiles().subscribe({
      next: (res: any) => {
        this.uploadedFiles = (res.files || []).map((file: any) => ({
          name: typeof file === 'string' ? file : file.name,
          size: typeof file === 'object' ? file.size : 0,
          uploadedAt: typeof file === 'object' ? new Date(file.uploadedAt) : new Date(),
        }));
        this.isLoadingFiles = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.isLoadingFiles = false;
        this.toast.error('Failed to load files', 'Could not retrieve uploaded files');
      },
    });
  }

  onFileSelected(event: any) {
    if (event.target.files && event.target.files.length > 0) {
      this.handleFile(event.target.files[0]);
    }
  }

  upload() {
    if (!this.selectedFile) {
      return;
    }

    const fileName = this.selectedFile.name;
    const fileSize = this.selectedFile.size;

    this.api.uploadFile(this.selectedFile).subscribe({
      next: () => {
        this.selectedFile = undefined!;
        this.toast.success(
          'Upload successful',
          `${fileName} (${this.formatFileSize(fileSize)}) uploaded successfully`
        );
        this.fetchUploadedFiles();
      },
      error: (err) => {
        let errorMessage = 'Upload failed. Please try again.';
        if (err.error?.detail) {
          errorMessage = err.error.detail;
        }
        this.toast.error('Upload failed', errorMessage);
      },
    });
  }

  deleteFile(fileName: string) {
    if (!confirm(`Are you sure you want to delete "${fileName}"?`)) {
      return;
    }

    this.api.deleteFile(fileName).subscribe({
      next: () => {
        this.toast.success('File deleted', `${fileName} has been removed`);
        this.fetchUploadedFiles();
      },
      error: (err) => {
        this.toast.error('Delete failed', 'Could not delete the file');
      },
    });
  }

  formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
  }

  getTimeAgo(date: Date): string {
    const seconds = Math.floor((new Date().getTime() - date.getTime()) / 1000);
    const intervals: { [key: string]: number } = {
      year: 31536000,
      month: 2592000,
      week: 604800,
      day: 86400,
      hour: 3600,
      minute: 60,
    };

    for (const [name, secondsInInterval] of Object.entries(intervals)) {
      const interval = Math.floor(seconds / secondsInInterval);
      if (interval >= 1) {
        return interval === 1 ? `1 ${name} ago` : `${interval} ${name}s ago`;
      }
    }
    return 'just now';
  }

  send() {
    if (!this.query.trim()) return;
    const question = this.query;
    this.messages.push({ sender: 'User', text: question });
    this.query = '';
    this.isLoading = true;
    this.loadingPhase = 'thinking';
    this.api.chatRag(question).subscribe({
      next: (res: any) => {
        this.loadingPhase = 'formatting';
        setTimeout(() => {
          let html: SafeHtml | string = res.answer || res.response || res.error;
          if (typeof html === 'string') {
            let rendered: string;
            if (typeof marked.parse === 'function') {
              const result = marked.parse(html);
              rendered = typeof result === 'string' ? result : (marked as any)(html);
            } else {
              rendered = (marked as any)(html);
            }
            html = this.sanitizer.bypassSecurityTrustHtml(rendered);
          }
          this.messages.push({ sender: 'AI', text: res.answer || res.response || res.error, html, sources: res.sources });
          this.isLoading = false;
          this.loadingPhase = 'none';
          this.cdr.detectChanges();
          setTimeout(() => this.scrollToBottom(), 100);
        }, 200);
      },
      error: (err) => {
        this.isLoading = false;
        this.loadingPhase = 'none';
        let errorMessage = 'Failed to get response';
        if (err.error?.detail) {
          errorMessage = err.error.detail;
        }
        this.toast.error('Error', errorMessage);
      }
    });
  }

  scrollToBottom() {
    setTimeout(() => {
      if (this.chatWindow) {
        this.chatWindow.nativeElement.scrollTop = this.chatWindow.nativeElement.scrollHeight;
      }
    }, 100);
  }

  handleFile(file: File) {
    if (!file.name.toLowerCase().endsWith('.pdf')) {
      this.toast.error('Invalid format', 'Only PDF files are allowed');
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      const fileSizeMB = Math.round((file.size / (1024 * 1024)) * 100) / 100;
      this.toast.error('File too large', `${fileSizeMB} MB exceeds 10 MB limit`);
      return;
    }
    this.selectedFile = file;
    this.upload();
  }
}
