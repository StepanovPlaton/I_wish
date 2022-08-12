import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { NOT_FOUND, PLUS } from 'src/app/shared/consts/images.consts';
import { IWish } from 'src/app/shared/models/http.model';
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
    private readonly wishListService: WishListService
  ) {
    this.wishListService.getWishes(this.login).subscribe((wishes) => {
      this.wishes = wishes;
    });
  }

  ngOnInit(): void {}
  openWish(wish: IWish) {
    this.router.navigate(['wish', wish.ID], {
      queryParams: {
        ...wish,
      },
    });
  }
}
