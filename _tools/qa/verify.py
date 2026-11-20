from math import *
def N(phi):
    if phi<=0: return 1.0, 2+pi, 0.0
    t=tan(radians(phi)); Nq=exp(pi*t)*tan(radians(45+phi/2))**2
    return Nq,(Nq-1)/t,2*(Nq-1)*t
print('N table')
for p in [0,10,15,20,24,26,28,30,32,35,40,45]:
    print(p, ' '.join(f'{x:.2f}' for x in N(p)))
def drained(Bp,Lp,gp,q,phi,c,Hk=0,Vk=1,m=None,alpha=0,strip=True,r=None):
    Nq,Nc,Ng=N(phi); t=tan(radians(phi))
    if strip: sg=sq=sc=1.0
    else:
        r=Bp/Lp if r is None else r
        sg=1-0.3*r; sq=1+r*sin(radians(phi)); sc=(sq*Nq-1)/(Nq-1)
    A=Bp*Lp
    f=Hk/(Vk+A*c/t) if Hk else 0
    if m is None: m=2 if strip else (2+Bp/Lp)/(1+Bp/Lp)
    ig=(1-f)**(m+1); iq=(1-f)**m; ic=(iq*Nq-1)/(Nq-1)
    a=radians(alpha); bq=(1-a*t)**2; bc=bq-(1-bq)/(Nc*t)
    tw=0.5*gp*Bp*Ng*sg*ig*bq; td=q*Nq*sq*iq*bq; tc=c*Nc*sc*ic*bc
    return dict(Nq=Nq,Nc=Nc,Ng=Ng,sg=sg,sq=sq,sc=sc,f=f,m=m,ig=ig,iq=iq,ic=ic,bq=bq,bc=bc,tw=tw,td=td,tc=tc,RkA=tw+td+tc,Rk=(tw+td+tc)*A,Rd=(tw+td+tc)*A/1.4)
def show(name,d): print(name, {k:round(v,4) for k,v in d.items()})
# MP1
for B in (1.1,1.3):
    Gf=(B-0.3)*0.5*17; Gb=B*0.6*25; Gk=220+Gf+Gb; Vd=1.35*Gk+1.5*70
    q=17*0.8+18*0.3
    d=drained(B,1,18,q,24,12); print(f'MP1 B={B}: Gf={Gf:.2f} Gb={Gb:.2f} Gk={Gk:.2f} Vd={Vd:.2f} q={q}'); show('  ',d)
# MP2
Gk=243.3; Vd=1.35*Gk+105; sig=(2+pi)*150+19; print('MP2 Vd',Vd,'sig',sig,'Rk',sig*1.1,'Rd',sig*1.1/1.4)
# MP3..7
def mp3(eq=0.3,sign=-1,gw_above=True,alpha=0):
    Gf=(1.3-0.3)*0.4*18; Gb=1.3*1.0*25; Gk=250+Gf+Gb; Vd=1.35*Gk+1.5*170; Vk=Gk+170; Hk=30
    e=abs(Hk*1.0+sign*170*eq)/Vk; Bp=1.3-2*e
    if gw_above: q=18*0.8+9*0.3+10*0.3; gp=10
    else:
        q=18*1.1+18*0.3; twd=1.4; gp=10+(18-10)*(twd/Bp-0.5)
    d=drained(Bp,1,gp,q,26,30,Hk,Vk,alpha=alpha)
    print(f' Gk={Gk} Vd={Vd:.2f} Vk={Vk} e={e:.4f} Bp={Bp:.4f} q={q:.2f} gp={gp:.3f}'); show('  ',d)
print('MP3'); mp3()
print('MP4'); mp3(gw_above=False)
print('MP5'); mp3(sign=+1)
print('MP6'); mp3(eq=0.5)
print('MP7'); mp3(alpha=5)
# MP8
Gf=(2*1.5-0.16)*0.4*18; Gb=2*1.5*1.2*25; Gk=1000+Gf+Gb; Vd=1.35*Gk; e=100*1.2/Gk; Bp=2-2*e
q=18*1.0+9*0.5+10*0.1
print(f'MP8 Gf={Gf:.2f} Gb={Gb} Gk={Gk:.2f} Vd={Vd:.1f} e={e:.4f} Bp={Bp:.4f} A={Bp*1.5:.3f} q={q}')
d=drained(Bp,1.5,10,q,32,0,100,Gk,strip=False); show(' B-dir (r=B/L, mB)',d)
d=drained(1.5,Bp,10,q,32,0,0,Gk,strip=False); show(' L-dir no H (r=L/B)',d)
# EC7-style: B'=min
r=1.5/Bp; rm=Bp/1.5; mB=(2+rm)/(1+rm)
d=drained(1.5,Bp,10,q,32,0,100,Gk,m=mB,strip=False); show(' EC7 swap (calc)',d)
# MP9
Nq,Nc,Ng=N(30); a=0.5*10*Ng; b=31.35*Nq; Rk=255*1.4
Bp=(-b+sqrt(b*b+4*a*Rk))/(2*a); print('MP9',a,b,Rk,Bp,(-b-sqrt(b*b+4*a*Rk))/(2*a),Bp+0.04)
# MP10
def earthE(K1,K2,L):
    s=lambda z: 18*min(z,1.0)+9*max(0,min(z,1.5)-1.0)+10*max(0,z-1.5)
    E=K1*(s(0.4)+s(1.0))/2*0.6+K1*(s(1.0)+s(1.5))/2*0.5+K2*(s(1.5)+s(1.6))/2*0.1
    return E*L
Ka1=tan(radians(30))**2; Ka2=tan(radians(45-14))**2
Ea=earthE(Ka1,Ka2,1.5); E0=earthE(0.5,1-sin(radians(28)),1.5)
Hd=1.35*Ea+150; Rd=320*tan(radians(28))/1.1
print(f'MP10 Ka1={Ka1:.3f} Ka2={Ka2:.3f} Ea={Ea:.3f} E0={E0:.3f} Hd={Hd:.2f} Rd={Rd:.2f} Rpd={E0/1.1:.2f} sum={Rd+E0/1.1:.2f}; undr Rd={3*65/1.1:.2f}; lim0.4Vd(1.35)={0.4*1.35*320:.1f} lim(1.0)={0.4*320}')
# MP11
Ka=tan(radians(45-16))**2; Kp=tan(radians(45+16))**2; s1=19.5*2.05; s2=s1+10.5*0.95
Ea=Ka*(s1+s2)/2*0.95*1.45; Ep=Kp*(s1+s2)/2*0.95*1.45; td=tan(radians(2/3*16)); Rd=490*td/1.1
print(f'MP11 Ka={Ka:.4f} Kp={Kp:.4f} s1={s1:.3f} s2={s2:.3f} sha={Ka*s1:.2f},{Ka*s2:.2f} shp={Kp*s1:.2f},{Kp*s2:.2f} Ea={Ea:.2f} Ep={Ep:.2f} Hd={1.35*Ea+375:.2f} tgd={td:.4f} Rd={Rd:.2f} Rpd={Ep/1.1:.2f} sum={Rd+Ep/1.1:.2f}')
