import { BreakpointObserver } from '@angular/cdk/layout';
import { Component, OnInit, ViewChild } from '@angular/core';
import { MatSidenav } from '@angular/material/sidenav';
import { MenuService } from '../../../_services/menu.service';
import { NavItem } from '../../../_models/nav';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-sidenav',
  templateUrl: './sidenav.component.html',
  styleUrl: './sidenav.component.scss'
})
export class SidenavComponent implements OnInit {

  public isSmallScreen = false;

  main = this.menuService.main;
  components = this.menuService.components;

  mainLength = 0;
  componentsLength = 0;
  displayComponentHeader = this.menuService.displayComponentHeader;

  constructor(
    breakpointObserver: BreakpointObserver,
    private menuService: MenuService,
    private router: Router
  ) {
    this.isSmallScreen = breakpointObserver.isMatched('(min-width: 1000px)');
    breakpointObserver.observe('(min-width: 1000px)').subscribe((result) => {
      this.isSmallScreen = result.matches;
    });
   }

  @ViewChild(MatSidenav)
  sidenav!: MatSidenav;

  ngOnInit(): void {
    setTimeout(() => {
      this.countMenuItems();
    });
  }

  countMenuItems() {
    this.main.forEach((item) => {
      setTimeout(() => {
        if (!item.disabled) {
          this.mainLength++;
        }
      });
      this.checkCurrentUrl(item);
    });
    
    this.components.forEach((item) => {
      setTimeout(() => {
        if (!item.disabled) {
          this.componentsLength++;
        }
      });
      this.checkCurrentUrl(item);
    });
  }

  checkCurrentUrl(item: NavItem): void {
    this.menuService.currentUrl.subscribe((url: string) => {
      if (item.route && url) {
        item.expanded = url.indexOf(`${item.route}`) === 0;
      }
    });
  }

  closeNav(snav: any): void {
    if (!this.isSmallScreen) {
      snav.close();
    }
  }
  
  goToHomePage(): void {
    this.router.navigate(['/home-page']);
  }
}
