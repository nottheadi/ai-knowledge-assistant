import { Routes } from '@angular/router';
import { App } from './app';
import { LoginComponent } from './features/auth/pages/login/login.component';
import { authGuard, loginGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  {
    path: 'login',
    component: LoginComponent,
    canActivate: [loginGuard],
  },
  {
    path: '',
    component: App,
    canActivate: [authGuard],
  },
  {
    path: '**',
    redirectTo: '',
  },
];

