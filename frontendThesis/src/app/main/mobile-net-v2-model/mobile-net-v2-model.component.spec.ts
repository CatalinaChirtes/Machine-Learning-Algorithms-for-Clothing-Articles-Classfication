import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MobileNetV2ModelComponent } from './mobile-net-v2-model.component';

describe('MobileNetV2ModelComponent', () => {
  let component: MobileNetV2ModelComponent;
  let fixture: ComponentFixture<MobileNetV2ModelComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MobileNetV2ModelComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(MobileNetV2ModelComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
