import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SafeHtml } from '@angular/platform-browser';

@Component({
  selector: 'app-message-bubble',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './message-bubble.component.html',
  styleUrls: ['./message-bubble.component.css'],
})
export class MessageBubbleComponent {
  @Input() sender: 'User' | 'AI' = 'User';
  @Input() text: string = '';
  @Input() html?: SafeHtml | string;
  @Input() sources?: any[];
}
