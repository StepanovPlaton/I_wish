import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthComponent } from './auth.component';
import { AuthRoutingModule } from './auth-routing.module';
import { IonicModule } from '@ionic/angular';
import { TranslateModule } from '@ngx-translate/core';
import { RegistrationComponent } from './registration/registration.component';
import { AuthorizationComponent } from './authorization/authorization.component';
import { PasswordInputWithEyeModule } from '../base/password-input-with-eye/password-input-with-eye.module';

@NgModule({
  imports: [
    CommonModule,
    AuthRoutingModule,
    IonicModule,
    TranslateModule,
    PasswordInputWithEyeModule,
  ],
  declarations: [
    AuthComponent,
    RegistrationComponent,
    AuthorizationComponent,
  ],
  exports: []
})
export class AuthModule { }
