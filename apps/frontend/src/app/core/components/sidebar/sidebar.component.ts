import { Component, signal, computed, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { ThemeService } from '../../services/theme.service';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.css'
})
export class SidebarComponent {
  @Input() isMobilePanel = false;
  @Output() closePanel = new EventEmitter<void>();

  username = signal('');
  isDark = computed(() => this.themeService.theme() === 'dark');

  constructor(
    private authService: AuthService,
    private themeService: ThemeService,
    private router: Router
  ) {
    const user = this.authService.getUser();
    if (user) {
      this.username.set(user.username);
    }
  }

  toggleTheme(): void {
    this.themeService.toggleTheme();
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }

  close(): void {
    this.closePanel.emit();
  }
}
