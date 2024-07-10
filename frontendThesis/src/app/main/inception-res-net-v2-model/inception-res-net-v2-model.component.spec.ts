import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InceptionResNetV2ModelComponent } from './inception-res-net-v2-model.component';

describe('InceptionResNetV2ModelComponent', () => {
  let component: InceptionResNetV2ModelComponent;
  let fixture: ComponentFixture<InceptionResNetV2ModelComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InceptionResNetV2ModelComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(InceptionResNetV2ModelComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
