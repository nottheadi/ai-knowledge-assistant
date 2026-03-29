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
  @Input() uploadError: string = '';
  @Input() dragOver: boolean = false;
  @Output() queryChange = new EventEmitter<string>();
  @Output() send = new EventEmitter<void>();
  @Output() fileSelected = new EventEmitter<any>();
  @Output() upload = new EventEmitter<void>();
  @Output() dragOverEvent = new EventEmitter<Event>();
  @Output() dragLeaveEvent = new EventEmitter<Event>();
  @Output() dropEvent = new EventEmitter<Event>();
}
