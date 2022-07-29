import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from '../shared/guards/auth.guard';

const routes: Routes = [
  {
    path: "main",
    canActivateChild: [AuthGuard],
    children: [
      {
        path: "",
        loadChildren: () =>
          import('./main/main.module').then((m) => m.MainModule),
      },
      {
        path: ":login",
        loadChildren: () =>
          import('./main/main.module').then((m) => m.MainModule),
      }
    ]
  },
  {
    path: "wish",
    canActivateChild: [AuthGuard],
    children: [
      {
        path: "",
        redirectTo: "wish/create",
        pathMatch: "full"
      },
      {
        path: ":id",
        loadChildren: () =>
          import('./wish/wish.module').then((m) => m.WishModule)
      }
    ],
  },
  {
    path: "profile",
    canActivateChild: [AuthGuard],
    children: [
      {
        path: ":login",
        loadChildren: () => 
          import('./profile/profile.module').then((m) => m.ProfileModule)
      }
    ]
  }
];

@NgModule({
  providers: [AuthGuard],
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PagesRoutingModule { }
