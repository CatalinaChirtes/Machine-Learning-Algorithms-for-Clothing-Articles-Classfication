import { TestBed } from '@angular/core/testing';
import { MenuService } from './menu.service';
import { DIALOG_SCROLL_STRATEGY, Dialog } from '@angular/cdk/dialog';
import { Overlay } from '@angular/cdk/overlay';
import { TranslateModule, TranslateService } from '@ngx-translate/core';
import { InjectionToken } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MAT_DIALOG_DATA, MAT_DIALOG_SCROLL_STRATEGY, MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MAT_SNACK_BAR_DATA, MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatCardModule } from '@angular/material/card';
import { MatMenuModule } from '@angular/material/menu';

describe('MenuService', () => {
  let service: MenuService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        Dialog,
        MatDialog,
        Overlay,
        MatSnackBar,
        {provide: InjectionToken, useValue:{}},
        {provide: MAT_SNACK_BAR_DATA, useValue:{}},
        {provide: MAT_DIALOG_DATA, useValue:{}},
        {provide: MAT_DIALOG_SCROLL_STRATEGY, useValue:{}},
        {provide: DIALOG_SCROLL_STRATEGY, useValue:{}},
	TranslateService
      ],
      imports: [
        MatCardModule,
        MatDialogModule,
        MatSnackBarModule,
        TranslateModule.forRoot(),
        MatMenuModule
      ]
    });
    service = TestBed.inject(MenuService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
