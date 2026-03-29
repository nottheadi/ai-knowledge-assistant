import { Injectable, signal, effect, inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';

@Injectable({
  providedIn: 'root'
})
export class ThemeService {
  theme = signal<'light' | 'dark'>('dark');
  private platformId = inject(PLATFORM_ID);
  private isInitialized = false;

  constructor() {
    // Only initialize in browser context, not during SSR
    if (isPlatformBrowser(this.platformId)) {
      this.initTheme();
      this.setupThemeEffect();
      this.isInitialized = true;
    }
  }

  private initTheme() {
    try {
      // Check localStorage first
      const saved = localStorage.getItem('docent-theme') as 'light' | 'dark' | null;
      if (saved) {
        this.theme.set(saved);
        this.applyTheme(saved);
        return;
      }

      // Fall back to OS preference
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      const initialTheme = prefersDark ? 'dark' : 'light';
      this.theme.set(initialTheme);
      this.applyTheme(initialTheme);
    } catch (error) {
      // Silently fail if localStorage is not available
      console.warn('Theme initialization: localStorage not available');
    }
  }

  private setupThemeEffect() {
    // Whenever theme signal changes, apply it immediately
    effect(() => {
      const currentTheme = this.theme();
      this.applyTheme(currentTheme);

      try {
        localStorage.setItem('docent-theme', currentTheme);
      } catch (error) {
        // Silently fail if localStorage is not available
        console.warn('Theme persistence: localStorage not available');
      }
    });
  }

  private applyTheme(theme: 'light' | 'dark') {
    try {
      const html = document.documentElement;

      // Remove both classes
      html.classList.remove('light-theme', 'dark-theme');

      // Add the active theme class
      html.classList.add(theme === 'light' ? 'light-theme' : 'dark-theme');

      // Set color-scheme for native UI elements
      html.style.colorScheme = theme;
    } catch (error) {
      // Silently fail if DOM is not available
      console.warn('Theme application: DOM not available');
    }
  }

  toggleTheme() {
    const newTheme = this.theme() === 'dark' ? 'light' : 'dark';
    this.theme.set(newTheme);
  }

  getTheme() {
    return this.theme();
  }

  isReady() {
    return this.isInitialized;
  }
}
