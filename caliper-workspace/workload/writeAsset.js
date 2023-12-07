'use strict';

const { WorkloadModuleBase } = require('@hyperledger/caliper-core');

class WriteAssetWorkload extends WorkloadModuleBase {
    async initializeWorkloadModule(workerIndex, totalWorkers, roundIndex, roundArguments, sutAdapter, sutContext) {
        await super.initializeWorkloadModule(workerIndex, totalWorkers, roundIndex, roundArguments, sutAdapter, sutContext);

        // No need to initialize assets during the initialization phase for the write workload
    }

    async submitTransaction() {
        const assetID = `${this.workerIndex}_write_${Date.now()}`;
        console.log(`Worker ${this.workerIndex}: Writing asset ${assetID}`);
        
        // Use parameters from your Go chaincode
        const request = {
            contractId: this.roundArguments.contractId,
            contractFunction: 'CreateAsset',
            invokerIdentity: 'User1',
            contractArguments: [assetID, 'blue', 'Tomoko', 'test'],  // Adjust based on your chaincode parameters
            readOnly: false
        };

        await this.sutAdapter.sendRequests(request);
    }

    async cleanupWorkloadModule() {
        for (let i = 0; i < this.roundArguments.assets; i++) {
            const assetID = `${this.workerIndex}_${i}`;
            console.log(`Worker ${this.workerIndex}: Deleting asset ${assetID}`);
            const request = {
                contractId: this.roundArguments.contractId,
                contractFunction: 'DeleteAsset',
                invokerIdentity: 'User1',
                contractArguments: [assetID],
                readOnly: false
            };

            await this.sutAdapter.sendRequests(request);
        }
    }
}

function createWorkloadModule() {
    return new WriteAssetWorkload();
}

module.exports.createWorkloadModule = createWorkloadModule;
