import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PagesRoutingModule } from './pages/pages-routing.module';
import { PagesModule } from './pages/pages.module';
import { AuthGuard } from './shared/guards/auth.guard';

const routes: Routes = [
  {
    path: "",
    loadChildren: () =>
          import('./pages/pages.module').then((m) => m.PagesModule),
    canActivate: [AuthGuard],
  },
  {
    path: "auth",
    loadChildren: () =>
      import('./auth/auth.module').then((m) => m.AuthModule),
  },
  {
    path: "**",
    redirectTo: ""
  }
];

@NgModule({
  providers: [AuthGuard],
  imports: [PagesRoutingModule, RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
