import { Component, ElementRef, signal, ViewChild, OnInit, ChangeDetectorRef } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { marked } from 'marked';
import { RouterOutlet } from '@angular/router';
import { ApiService } from './services/api.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, FormsModule, CommonModule],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App implements OnInit {
  protected readonly title = signal('frontend');

  selectedFile!: File;

  uploadedFiles: string[] = [];

  query = '';

  messages: any[] = [];

  isLoading = false;
  loadingPhase: 'none' | 'thinking' | 'refining' | 'formatting' = 'none';

  @ViewChild('chatWindow') chatWindow!: ElementRef;

  constructor(
    private api: ApiService,
    private cdr: ChangeDetectorRef,
    private sanitizer: DomSanitizer,
  ) {}

  ngOnInit(): void {
    this.fetchUploadedFiles();
  }
  fetchUploadedFiles() {
    console.log('Fetching uploaded files...');
    this.api.getUploadedFiles().subscribe({
      next: (res: any) => {
        console.log('Files response:', res);
        this.uploadedFiles = res.files || [];
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Error fetching files:', err);
      },
    });
  }

  onFileSelected(event: any) {
    if (event.target.files && event.target.files.length > 0) {
      this.handleFile(event.target.files[0]);
    }
  }

  upload() {
    this.uploadError = '';
    if (!this.selectedFile) {
      this.uploadError = 'Please select a file first.';
      return;
    }
    this.api.uploadFile(this.selectedFile).subscribe({
      next: () => {
        this.selectedFile = undefined!;
        this.fetchUploadedFiles();
      },
      error: (err) => {
        this.uploadError = 'Upload failed. Please try again.';
      },
    });
  }

  send() {
    if (!this.query.trim()) return;

    const question = this.query;

    this.messages.push({
      sender: 'User',
      text: question,
    });

    this.query = '';

    this.isLoading = true;
    this.loadingPhase = 'thinking';

    const start = performance.now();
    this.api.chatRag(question).subscribe((res: any) => {
      // API responded, now formatting
      this.loadingPhase = 'formatting';
      // If Markdown processing is fast, show the phase only briefly
      setTimeout(() => {
        let html: SafeHtml | string = res.answer || res.response || res.error;
        if (typeof html === 'string') {
          let rendered: string;
          if (typeof marked.parse === 'function') {
            const result = marked.parse(html);
            if (typeof result === 'string') {
              rendered = result;
            } else {
              rendered = (marked as any)(html);
            }
          } else {
            rendered = (marked as any)(html);
          }
          html = this.sanitizer.bypassSecurityTrustHtml(rendered);
        }
        this.messages.push({
          sender: 'AI',
          text: res.answer || res.response || res.error,
          html: html,
          sources: res.sources,
        });
        this.isLoading = false;
        this.loadingPhase = 'none';
        setTimeout(() => this.scrollToBottom(), 100);
      }, 200); // Show 'Formatting response...' for at least 200ms
    });
  }

  scrollToBottom() {
    setTimeout(() => {
      if (this.chatWindow) {
        this.chatWindow.nativeElement.scrollTop = this.chatWindow.nativeElement.scrollHeight;
      }
    }, 100);
  }
  dragOver: boolean = false;
  uploadError: string = '';
  onDragOver(event: Event) {
    event.preventDefault();
    this.dragOver = true;
  }

  onDragLeave(event: Event) {
    event.preventDefault();
    this.dragOver = false;
  }

  onDrop(event: Event) {
    event.preventDefault();
    this.dragOver = false;
    const dragEvent = event as DragEvent;
    if (dragEvent.dataTransfer && dragEvent.dataTransfer.files.length > 0) {
      this.handleFile(dragEvent.dataTransfer.files[0]);
    }
  }

  handleFile(file: File) {
    this.uploadError = '';
    if (!file.name.toLowerCase().endsWith('.pdf')) {
      this.uploadError = 'Only PDF files are allowed.';
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      this.uploadError = 'File size exceeds 10 MB limit.';
      return;
    }
    this.selectedFile = file;
  }
}
