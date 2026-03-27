import { Component, Output, EventEmitter, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-chat-input',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat-input.component.html',
  styleUrls: ['./chat-input.component.css'],
})
export class ChatInputComponent {
  @Input() query: string = '';
  @Input() selectedFile: File | undefined;
  @Output() queryChange = new EventEmitter<string>();
  @Output() send = new EventEmitter<void>();
  @Output() fileSelected = new EventEmitter<any>();
}
