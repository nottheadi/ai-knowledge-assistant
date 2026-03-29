import { Component, ElementRef, signal, ViewChild, ChangeDetectorRef, afterNextRender } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { marked } from 'marked';
import { Router, RouterOutlet } from '@angular/router';
import { ApiService } from './core/services/api.service';
import { AuthService } from './core/services/auth.service';
import { ThemeService } from './core/services/theme.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

import { SidebarComponent } from './core/components/sidebar/sidebar.component';
import { MessageListComponent } from './features/chat/components/message-list/message-list.component';
import { ChatInputComponent } from './features/chat/components/chat-input/chat-input.component';
import { UploadedFile } from './features/knowledge-base/models/uploaded-file.model';
import { Message } from './features/chat/models/message.model';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, FormsModule, CommonModule, SidebarComponent, MessageListComponent, ChatInputComponent],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {
  protected readonly title = signal('frontend');

  selectedFile!: File;
  uploadedFiles: UploadedFile[] = [];
  query = '';
  messages: Message[] = [];
  isLoading = false;
  loadingPhase: 'none' | 'thinking' | 'refining' | 'formatting' = 'none';
  toastMessage: string = '';
  toastType: 'success' | 'error' | 'info' = 'info';
  toastFadingOut: boolean = false;
  private toastTimeout: ReturnType<typeof setTimeout> | null = null;
  dragOver: boolean = false;
  uploadError: string = '';
  isLoggedIn: boolean = false;

  @ViewChild('chatWindow') chatWindow!: ElementRef;

  constructor(
    private api: ApiService,
    public authService: AuthService,
    private router: Router,
    private cdr: ChangeDetectorRef,
    private sanitizer: DomSanitizer,
    public themeService: ThemeService,
  ) {
    this.isLoggedIn = this.authService?.isAuthenticated() ?? false;

    afterNextRender(() => {
      if (this.authService.isAuthenticated()) {
        this.fetchUploadedFiles();
      }
    });

    this.authService.isAuthenticated$.subscribe((isAuthenticated) => {
      this.isLoggedIn = isAuthenticated;
      if (isAuthenticated) {
        this.fetchUploadedFiles();
      } else {
        this.uploadedFiles = [];
      }
    });
  }

  fetchUploadedFiles() {
    if (!this.authService.isAuthenticated()) {
      return;
    }

    this.api.getUploadedFiles().subscribe({
      next: (res: any) => {
        this.uploadedFiles = (res.files || []).map((name: string) => ({
          name,
          status: 'uploaded' as const,
        }));
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
    if (!this.authService.isAuthenticated()) {
      this.router.navigate(['/login']);
      return;
    }

    this.uploadError = '';
    if (!this.selectedFile) {
      this.uploadError = 'Please select a file first.';
      return;
    }
    const fileName = this.selectedFile.name;
    const fileToUpload = this.selectedFile;
    this.selectedFile = undefined!;

    // Add pill in uploading state immediately
    this.uploadedFiles = [...this.uploadedFiles, { name: fileName, status: 'uploading' }];
    this.cdr.detectChanges();

    this.api.uploadFile(fileToUpload).subscribe({
      next: () => {
        this.uploadedFiles = this.uploadedFiles.map(f =>
          f.name === fileName ? { ...f, status: 'uploaded' as const } : f
        );
        this.showToast(`${fileName} uploaded successfully`, 'success');
      },
      error: () => {
        this.uploadedFiles = this.uploadedFiles.filter(f => f.name !== fileName);
        this.uploadError = 'Upload failed. Please try again.';
        this.cdr.detectChanges();
      },
    });
  }

  deleteFile(fileName: string) {
    if (!this.authService.isAuthenticated()) {
      this.router.navigate(['/login']);
      return;
    }

    // Switch pill to deleting state immediately
    this.uploadedFiles = this.uploadedFiles.map(f =>
      f.name === fileName ? { ...f, status: 'deleting' as const } : f
    );
    this.cdr.detectChanges();

    this.api.deleteFile(fileName).subscribe({
      next: () => {
        this.uploadedFiles = this.uploadedFiles.filter(f => f.name !== fileName);
        this.showToast(`${fileName} deleted`, 'success');
      },
      error: () => {
        this.uploadedFiles = this.uploadedFiles.map(f =>
          f.name === fileName ? { ...f, status: 'uploaded' as const } : f
        );
        this.showToast('Failed to delete file', 'error');
      },
    });
  }

  send() {
    if (!this.authService.isAuthenticated()) {
      this.router.navigate(['/login']);
      return;
    }

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
        this.showToast('Unable to get response from server', 'error');
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
    this.upload();
  }

  showToast(message: string, type: 'success' | 'error' | 'info' = 'info') {
    // Clear any existing toast timeout
    if (this.toastTimeout) {
      clearTimeout(this.toastTimeout);
    }
    this.toastMessage = message;
    this.toastType = type;
    this.toastFadingOut = false;
    this.cdr.detectChanges();

    this.toastTimeout = setTimeout(() => {
      this.toastFadingOut = true;
      this.cdr.detectChanges();
      // Wait for fade-out animation to finish
      setTimeout(() => {
        this.toastMessage = '';
        this.toastFadingOut = false;
        this.cdr.detectChanges();
      }, 350);
    }, 2700);
  }
}
