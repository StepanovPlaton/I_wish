import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { WishListComponent } from './wish-list.component';
import { IonicModule } from '@ionic/angular';
import { TranslateModule } from '@ngx-translate/core';
import { RouterModule } from '@angular/router';

@NgModule({
  declarations: [WishListComponent],
  imports: [CommonModule, IonicModule, TranslateModule, RouterModule],
  exports: [WishListComponent],
})
export class WishListModule {}
