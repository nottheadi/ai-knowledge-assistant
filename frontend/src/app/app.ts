import { Component, ElementRef, signal, ViewChild, OnInit, ChangeDetectorRef } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ApiService } from './services/api.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';


@Component({
  selector: 'app-root',
  imports: [RouterOutlet, FormsModule, CommonModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {
  protected readonly title = signal('frontend');

  selectedFile!: File;

  uploadedFiles: string[] = [];

  query = '';

  messages: any[] = [];

  isLoading = false;

  @ViewChild('chatWindow') chatWindow!: ElementRef;

  constructor(private api: ApiService, private cdr: ChangeDetectorRef) {}

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
      }
    });
  }

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
  }

  upload() {

    if (!this.selectedFile) {
      alert("Please select a file first");
      return;
    }

    this.api.uploadFile(this.selectedFile).subscribe(() => {
      alert("File uploaded successfully");
      this.fetchUploadedFiles();
    });

  }

  send() {

    if (!this.query.trim()) return;

    const question = this.query;

    this.messages.push({
      sender: 'User',
      text: question
    });

    this.query = '';

    this.isLoading = true;

    this.api.chat(question).subscribe((res: any) => {
      console.log('Chat API response:', res);
      this.isLoading = false;
      this.messages.push({
        sender: 'AI',
        text: res.response, // Use the correct property from backend
        sources: res.sources
      });
      setTimeout(() => this.scrollToBottom(), 100);
    });

  }

  scrollToBottom() {

    setTimeout(() => {

      if (this.chatWindow) {
        this.chatWindow.nativeElement.scrollTop =
          this.chatWindow.nativeElement.scrollHeight;
      }

    }, 100);

  }
}