import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { pluck, switchMap } from 'rxjs';
import { NOT_FOUND, PLUS } from '../../shared/consts/images.consts';
import { IWish } from '../../shared/models/http.model';
import { ApiService } from '../../shared/services/api.service';
import { AuthService } from '../../shared/services/auth.service';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss']
})
export class MainComponent implements OnInit {
  NOT_FOUND = NOT_FOUND;
  PLUS = PLUS

  wishes: IWish[] | null = null;
  login: string | undefined;

  constructor(
    private readonly authService: AuthService,
    private readonly apiService: ApiService,
    private readonly router: Router,
    private readonly activatedRoute: ActivatedRoute,
  ) {
    this.activatedRoute.params.pipe(
      pluck('login'),
      switchMap(login => {
        this.login = login
        return this.apiService.getWishes(login)
      })
    ).subscribe((wishes) => {
      this.wishes = wishes
    })
  }

  ngOnInit() {
  }

  openWish(wish: IWish) {
    this.router.navigate(["wish", wish.ID])
  }

  addWish() {
    this.router.navigate(["wish", "create"])
  }
}
