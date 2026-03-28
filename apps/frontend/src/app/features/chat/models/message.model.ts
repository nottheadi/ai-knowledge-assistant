import { SafeHtml } from '@angular/platform-browser';

export interface Message {
  sender: 'User' | 'AI';
  text: string;
  html?: SafeHtml | string;
  sources?: Array<{ page: number; source: string }>;
}
