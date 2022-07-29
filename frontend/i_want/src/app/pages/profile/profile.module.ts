import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';
import { TranslateModule } from '@ngx-translate/core';
import { PasswordInputWithEyeModule } from '../../base/password-input-with-eye/password-input-with-eye.module';
import { ProfileComponent } from './profile.component';
import { ProfileRoutingModule } from './profile-routing.component';

@NgModule({
  imports: [
    CommonModule,
    IonicModule,
    ProfileRoutingModule,
    TranslateModule,
    PasswordInputWithEyeModule,
  ],
  declarations: [
    ProfileComponent
  ],
  exports: []
})
export class ProfileModule { }
