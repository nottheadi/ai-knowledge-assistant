import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

export interface Toast {
  id: string;
  type: 'success' | 'error' | 'info' | 'warning';
  title: string;
  message: string;
  duration?: number; // ms, 0 = indefinite
  dismissible?: boolean;
}

@Injectable({
  providedIn: 'root',
})
export class ToastService {
  private toasts = new BehaviorSubject<Toast[]>([]);
  public toasts$ = this.toasts.asObservable();

  private toastCounter = 0;

  success(title: string, message: string, duration = 3000) {
    this.add({ type: 'success', title, message, duration, dismissible: true });
  }

  error(title: string, message: string, duration = 0) {
    this.add({ type: 'error', title, message, duration, dismissible: true });
  }

  info(title: string, message: string, duration = 3000) {
    this.add({ type: 'info', title, message, duration, dismissible: true });
  }

  warning(title: string, message: string, duration = 4000) {
    this.add({ type: 'warning', title, message, duration, dismissible: true });
  }

  private add(toast: Omit<Toast, 'id'>) {
    const id = `toast-${++this.toastCounter}`;
    const newToast: Toast = { ...toast, id };
    const currentToasts = this.toasts.value;
    this.toasts.next([...currentToasts, newToast]);

    if (toast.duration && toast.duration > 0) {
      setTimeout(() => this.dismiss(id), toast.duration);
    }
  }

  dismiss(id: string) {
    this.toasts.next(this.toasts.value.filter(t => t.id !== id));
  }

  clearAll() {
    this.toasts.next([]);
  }
}
