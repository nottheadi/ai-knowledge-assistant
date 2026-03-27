import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ToastService, Toast } from '../services/toast.service';

@Component({
  selector: 'app-toast-container',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="toast-container">
      <div
        *ngFor="let toast of toasts"
        [ngClass]="'toast toast-' + toast.type"
        [@toast]
        class="toast-item"
      >
        <div class="toast-content">
          <div class="toast-title">{{ toast.title }}</div>
          <div class="toast-message">{{ toast.message }}</div>
        </div>
        <button
          *ngIf="toast.dismissible"
          (click)="dismiss(toast.id)"
          class="toast-close"
          aria-label="Close notification"
        >
          ✕
        </button>
      </div>
    </div>
  `,
  styles: [`
    .toast-container {
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 9999;
      pointer-events: none;
    }

    .toast-item {
      pointer-events: auto;
      margin-bottom: 12px;
      animation: slideIn 0.3s ease-out forwards;
    }

    @keyframes slideIn {
      from {
        transform: translateX(400px);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }

    .toast {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding: 12px 16px;
      border-radius: 0.75rem;
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.2);
      box-shadow: 0 4px 24px rgba(0, 0, 0, 0.15);
      max-width: 380px;
      min-width: 300px;
      font-size: 0.95rem;
    }

    .toast-success {
      background: rgba(34, 197, 94, 0.95);
      color: white;
      border-color: rgba(34, 197, 94, 0.5);
    }

    .toast-error {
      background: rgba(239, 68, 68, 0.95);
      color: white;
      border-color: rgba(239, 68, 68, 0.5);
    }

    .toast-info {
      background: rgba(59, 130, 246, 0.95);
      color: white;
      border-color: rgba(59, 130, 246, 0.5);
    }

    .toast-warning {
      background: rgba(245, 158, 11, 0.95);
      color: white;
      border-color: rgba(245, 158, 11, 0.5);
    }

    .toast-content {
      flex: 1;
      display: flex;
      flex-direction: column;
    }

    .toast-title {
      font-weight: 600;
      margin-bottom: 4px;
    }

    .toast-message {
      font-size: 0.9rem;
      opacity: 0.95;
    }

    .toast-close {
      background: none;
      border: none;
      color: inherit;
      cursor: pointer;
      font-size: 1.2rem;
      padding: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      width: 24px;
      height: 24px;
      opacity: 0.8;
      transition: opacity 0.2s;
      flex-shrink: 0;
    }

    .toast-close:hover {
      opacity: 1;
    }

    @media (max-width: 640px) {
      .toast-container {
        top: 10px;
        right: 10px;
        left: 10px;
      }

      .toast {
        min-width: auto;
        max-width: 100%;
      }
    }
  `]
})
export class ToastContainerComponent implements OnInit {
  toasts: Toast[] = [];

  constructor(private toastService: ToastService) {}

  ngOnInit() {
    this.toastService.toasts$.subscribe(toasts => {
      this.toasts = toasts;
    });
  }

  dismiss(id: string) {
    this.toastService.dismiss(id);
  }
}
