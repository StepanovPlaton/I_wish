import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { NOT_FOUND, PLUS } from 'src/app/shared/consts/images.consts';
import { IWish } from 'src/app/shared/models/http.model';
import { AuthService } from 'src/app/shared/services/auth.service';
import { WishListService } from './wish-list.service';

@Component({
  selector: 'app-wish-list',
  templateUrl: './wish-list.component.html',
  styleUrls: ['./wish-list.component.scss'],
})
export class WishListComponent implements OnInit {
  NOT_FOUND = NOT_FOUND;
  PlUS = PLUS;

  wishes: IWish[] | null = null;

  @Input()
  login: string | undefined;

  constructor(
    private readonly router: Router,
    private readonly wishListService: WishListService,
    private readonly authService: AuthService
  ) {}

  ngOnInit(): void {
    this.wishListService.getWishes(this.login).subscribe((wishes) => {
      this.wishes = wishes.filter((wish) => {
        if (!this.login) {
          if (!wish.HidingDate) return true;
          return new Date().getTime() < new Date(wish.HidingDate).getTime();
        } else {
          if (this.authService.userAuthorizationData) {
            if (this.login === this.authService.userAuthorizationData.login) {
              return true;
            } else {
              if (!wish.HidingDate) return true;
              return new Date().getTime() < new Date(wish.HidingDate).getTime();
            }
          } else return true;
        }
      });
    });
  }
  openWish(wish: IWish) {
    this.router.navigate(['wish', wish.ID], {
      queryParams: {
        ...wish,
      },
    });
  }
}
