import { Injectable } from '@angular/core';
import { map } from 'rxjs';
import { IWish } from 'src/app/shared/models/http.model';
import { ApiService } from 'src/app/shared/services/api.service';

@Injectable({
  providedIn: 'root',
})
export class WishListService {
  wishes: IWish[] | null = null;

  constructor(private readonly apiService: ApiService) {}

  getWishes(login?: string) {
    return this.apiService.getWishes(login).pipe(
      map((wishes) => {
        this.wishes = wishes;
        return wishes;
      })
    );
  }

  getNextWish(id: number): IWish | null {
    if (this.wishes) {
      if (this.wishes[this.wishes.length - 1].ID === id) {
        return this.wishes[0];
      } else {
        const i = this.wishes.findIndex((wish) => {
          if (wish.ID === id) return true;
          return false;
        });
        if (i === -1) return null;
        return this.wishes[i + 1];
      }
    } else {
      this.getWishes();
      return this.getNextWish(id);
    }
  }
  getPreviousWish(id: number): IWish | null {
    if (this.wishes) {
      if (this.wishes[0].ID === id) {
        return this.wishes[this.wishes.length - 1];
      } else {
        const i = this.wishes.findIndex((wish) => {
          if (wish.ID === id) return true;
          return false;
        });
        if (i === -1) return null;
        return this.wishes[i - 1];
      }
    } else {
      this.getWishes();
      return this.getPreviousWish(id);
    }
  }
}
