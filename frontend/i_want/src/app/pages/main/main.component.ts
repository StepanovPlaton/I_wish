import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { pluck } from 'rxjs';
import { NOT_FOUND, PLUS } from '../../shared/consts/images.consts';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss'],
})
export class MainComponent implements OnInit {
  NOT_FOUND = NOT_FOUND;
  PLUS = PLUS;

  login: string | undefined;

  constructor(
    private readonly router: Router,
    private readonly activatedRoute: ActivatedRoute
  ) {
    this.activatedRoute.params
      .pipe(pluck('login'))
      .subscribe((login) => (this.login = login));
  }

  ngOnInit() {}

  addWish() {
    this.router.navigate(['wish', 'create']);
  }
}
