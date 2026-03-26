import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MessageBubbleComponent } from './message-bubble.component';

@Component({
  selector: 'app-message-list',
  standalone: true,
  imports: [CommonModule, MessageBubbleComponent],
  templateUrl: './message-list.component.html',
  styleUrls: ['./message-list.component.css'],
})
export class MessageListComponent {
  @Input() messages: any[] = [];
  @Input() isLoading: boolean = false;
  @Input() loadingPhase: string = 'none';
}
