% Noise simulation on ECG.
% Codes are obtained from 'testNoiseGenerator.m'.
% SK changed the weight of muscle artifact noise to 5.


clc
clear
close all;

% load('SampleECG1.mat');
load('SampleECG2.mat'); data = data(1:15000,6)';

fs = 1000;
N = length(data);

% baseline wander removal
bsline = LPFilter(data,.7/fs);          % baseline wander removal (may be replaced by other approaches)
%bsline = BaseLineKF(data,.5/fs);       % baseline wander removal (may be replaced by other approaches)
data = data-bsline;

t = (0:N-1)/fs;

% noise variance calculation
SNR = 5;
SignalPower = mean(data.^2);
NoisePower = SignalPower / 10^(SNR/10);

noisetype = 5;

beta = 1.5;     % noise color (for noisetype = 1)
w_bw = 1;       % weight of baseline wander noise in the generated noise (for noisetype = 5)
w_em = 1;       % weight of electrode movement noise in the generated noise (for noisetype = 5)
w_ma = 5;       % weight of muscle artifact noise in the generated noise (for noisetype = 5)

switch noisetype
    case 0     % white noise
        noise = sqrt(NoisePower)*randn(size(data));
        
    case 1     % colored noise
        noise = ColoredNoise(sqrt(NoisePower),N,fs,beta);
        
    case 2     % real muscle artifacts
        load('MA.mat');artifact = MA(:,2);
        artifact = resample(artifact,fs,360);
        artifact = artifact(1:N)';
        noise = sqrt(NoisePower)*(artifact - mean(artifact))/std(artifact,1);
        
    case 3     % real electrode movements
        load('EM.mat');artifact = EM(:,3);
        artifact = resample(artifact,fs,360);
        artifact = artifact(1:N)';
        noise = sqrt(NoisePower)*(artifact - mean(artifact))/std(artifact,1);
        
    case 4     % real baseline wander
        load('BW.mat');artifact = BW(:,3);
        artifact = resample(artifact,fs,360);
        artifact = artifact(1:N)';
        noise = sqrt(NoisePower)*(artifact - mean(artifact))/std(artifact,1);
    
    case 5     % mixture of real baseline wander, electrode movements, muscle artifacts
        load('BW.mat'); bw = BW(:,3);    bw = (bw-mean(bw))/std(bw);
        load('EM.mat'); em = EM(:,3);    em = (em-mean(em))/std(em);
        load('MA.mat'); ma = MA(:,3);    ma = (ma-mean(ma))/std(ma);
        artifact = (w_bw*bw + w_em*em + w_ma*ma)/(w_bw + w_em + w_ma);
        artifact = resample(artifact,fs,360);
        artifact = artifact(1:N)';
        noise = sqrt(NoisePower)*(artifact - mean(artifact))/std(artifact,1);
end

x = data + noise;

figure;
plot(t,noise);
grid;

figure;
plot(t,x,'r');
hold on
plot(t,data,'b');
grid;
xlabel('time (sec.)');
legend('Noisy ECG','Original ECG');
