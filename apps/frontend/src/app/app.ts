import { Component, ElementRef, signal, ViewChild, OnInit, ChangeDetectorRef } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { marked } from 'marked';
import { RouterOutlet } from '@angular/router';
import { ApiService } from './services/api.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

import { MessageListComponent } from './components/message-list.component';
import { ChatInputComponent } from './components/chat-input.component';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, FormsModule, CommonModule, MessageListComponent, ChatInputComponent],
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

  toastMessage: string = '';

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
    this.api.getUploadedFiles().subscribe({
      next: (res: any) => {
        this.uploadedFiles = res.files || [];
        this.cdr.detectChanges();
      },
      error: () => {},
    });
  }

  onFileSelected(event: any) {
    if (event.target.files && event.target.files.length > 0) {
      this.handleFile(event.target.files[0]);
      event.target.value = '';
    }
  }

  upload() {
    this.uploadError = '';
    if (!this.selectedFile) {
      this.uploadError = 'Please select a file first.';
      return;
    }
    const fileName = this.selectedFile.name;
    this.api.uploadFile(this.selectedFile).subscribe({
      next: () => {
        this.selectedFile = undefined!;
        this.toastMessage = `✓ ${fileName} uploaded successfully`;
        this.cdr.detectChanges();
        setTimeout(() => { this.toastMessage = ''; this.cdr.detectChanges(); }, 3000);
        this.fetchUploadedFiles();
      },
      error: () => {
        this.uploadError = 'Upload failed. Please try again.';
        this.cdr.detectChanges();
      },
    });
  }

  deleteFile(fileName: string) {
    this.api.deleteFile(fileName).subscribe({
      next: () => {
        this.toastMessage = `✓ ${fileName} deleted`;
        this.cdr.detectChanges();
        setTimeout(() => { this.toastMessage = ''; this.cdr.detectChanges(); }, 3000);
        this.fetchUploadedFiles();
      },
      error: () => {
        this.toastMessage = 'Failed to delete file.';
        this.cdr.detectChanges();
        setTimeout(() => { this.toastMessage = ''; this.cdr.detectChanges(); }, 3000);
      },
    });
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
      error: () => {
        this.isLoading = false;
        this.loadingPhase = 'none';
        this.toastMessage = 'Error: Unable to get response from server.';
        this.cdr.detectChanges();
        setTimeout(() => { this.toastMessage = ''; this.cdr.detectChanges(); }, 3000);
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
    if (file) {
      this.upload();
    }
  }
}
